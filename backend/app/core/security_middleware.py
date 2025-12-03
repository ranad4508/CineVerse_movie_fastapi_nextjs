from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import time
from .security_detector import spam_detector, BotDetector
from .rate_limiter import RATE_LIMITS
import logging


logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    EXCLUDED_PATHS = ["/docs", "/openapi.json", "/redoc", "/health", "/.well-known"]
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        is_excluded = any(request.url.path.startswith(path) for path in self.EXCLUDED_PATHS)
        
        if not is_excluded:
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["X-Frame-Options"] = "SAMEORIGIN"
            response.headers["X-XSS-Protection"] = "1; mode=block"
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
            response.headers["Content-Security-Policy"] = "default-src 'self' https: 'unsafe-inline' 'unsafe-eval'"
            response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        return response


class SpamDetectionMiddleware(BaseHTTPMiddleware):
    EXCLUDED_PATHS = ["/docs", "/openapi.json", "/redoc", "/health", "/.well-known", "/favicon.ico"]
    
    async def dispatch(self, request: Request, call_next):
        if any(request.url.path.startswith(path) for path in self.EXCLUDED_PATHS):
            return await call_next(request)
        
        is_spam, spam_score = spam_detector.detect_spam(request)
        
        if is_spam:
            client_ip = request.client.host if request.client else "unknown"
            logger.warning(
                f"Spam/Bot detected from {client_ip}. Spam score: {spam_score}. "
                f"Path: {request.url.path}"
            )
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": "Suspicious activity detected. Access denied."}
            )
        
        if spam_score > 40:
            logger.info(f"High spam score ({spam_score}) for {request.client.host}: {request.url.path}")
        
        response = await call_next(request)
        response.headers["X-Spam-Score"] = str(min(spam_score, 100))
        
        return response


class RequestTimeoutMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            return response
        except Exception as e:
            logger.error(f"Request processing error: {str(e)}")
            raise


class RequestValidationMiddleware(BaseHTTPMiddleware):
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
    EXCLUDED_PATHS = ["/docs", "/openapi.json", "/redoc", "/health", "/.well-known", "/favicon.ico"]
    
    async def dispatch(self, request: Request, call_next):
        if any(request.url.path.startswith(path) for path in self.EXCLUDED_PATHS):
            return await call_next(request)
        
        if request.method in ["POST", "PUT", "PATCH"]:
            content_length = request.headers.get("content-length")
            if content_length:
                try:
                    if int(content_length) > self.MAX_CONTENT_LENGTH:
                        return JSONResponse(
                            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                            content={"detail": "Request body too large"}
                        )
                except ValueError:
                    pass
        
        user_agent = request.headers.get("user-agent", "")
        if not user_agent or BotDetector.is_bot(user_agent):
            if not any(request.url.path.startswith(path) for path in ["/api/v1/auth", "/health"]):
                if not user_agent:
                    logger.warning(f"Request without user-agent from {request.client.host}")
        
        response = await call_next(request)
        return response


class IPWhitelistMiddleware(BaseHTTPMiddleware):
    EXCLUDED_PATHS = ["/docs", "/openapi.json", "/redoc", "/health", "/.well-known", "/favicon.ico"]
    
    def __init__(self, app, whitelist: list = None):
        super().__init__(app)
        self.whitelist = whitelist or []
    
    async def dispatch(self, request: Request, call_next):
        if any(request.url.path.startswith(path) for path in self.EXCLUDED_PATHS):
            return await call_next(request)
        
        if self.whitelist:
            client_ip = request.client.host if request.client else "unknown"
            if client_ip not in self.whitelist:
                if request.url.path.startswith("/api/v1/admin"):
                    return JSONResponse(
                        status_code=status.HTTP_403_FORBIDDEN,
                        content={"detail": "Access denied. IP not whitelisted."}
                    )
        
        response = await call_next(request)
        return response
