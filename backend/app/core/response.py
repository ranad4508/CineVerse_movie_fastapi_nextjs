from pydantic import BaseModel
from typing import Optional, Any, List
from datetime import datetime


class ResponseMessage(BaseModel):
    status: str
    message: str
    code: int
    timestamp: datetime = None
    
    def __init__(self, **data):
        super().__init__(**data)
        if self.timestamp is None:
            self.timestamp = datetime.now()


class SuccessResponse(BaseModel):
    success: bool = True
    message: str
    data: Optional[Any] = None
    timestamp: datetime = None
    
    def __init__(self, message: str = "Success", data: Any = None, **kwargs):
        super().__init__(
            success=True,
            message=message,
            data=data,
            timestamp=datetime.now(),
            **kwargs
        )


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    error: Optional[str] = None
    code: Optional[int] = None
    timestamp: datetime = None
    
    def __init__(self, message: str = "Error", error: str = None, code: int = None, **kwargs):
        super().__init__(
            success=False,
            message=message,
            error=error,
            code=code,
            timestamp=datetime.now(),
            **kwargs
        )


class PaginatedResponse(BaseModel):
    success: bool = True
    message: str
    data: List[Any]
    pagination: dict
    timestamp: datetime = None
    
    def __init__(self, message: str = "Success", data: List[Any] = None, skip: int = 0, limit: int = 20, total: int = 0, **kwargs):
        super().__init__(
            success=True,
            message=message,
            data=data or [],
            pagination={
                "skip": skip,
                "limit": limit,
                "total": total,
                "pages": (total + limit - 1) // limit if limit > 0 else 0
            },
            timestamp=datetime.now(),
            **kwargs
        )


class ValidationError(BaseModel):
    success: bool = False
    message: str = "Validation error"
    errors: List[dict]
    code: int = 422
    timestamp: datetime = None
    
    def __init__(self, errors: List[dict], message: str = "Validation error", **kwargs):
        super().__init__(
            success=False,
            message=message,
            errors=errors,
            code=422,
            timestamp=datetime.now(),
            **kwargs
        )


RESPONSE_MESSAGES = {
    "created": "Resource created successfully",
    "updated": "Resource updated successfully",
    "deleted": "Resource deleted successfully",
    "retrieved": "Resource retrieved successfully",
    "not_found": "Resource not found",
    "invalid_input": "Invalid input provided",
    "unauthorized": "Unauthorized access",
    "forbidden": "Access forbidden",
    "server_error": "Internal server error",
    "rate_limit": "Rate limit exceeded",
    "duplicate": "Resource already exists",
    "invalid_credentials": "Invalid email or password",
    "email_exists": "Email already registered",
    "username_exists": "Username already taken",
    "user_inactive": "User account is inactive",
    "invalid_token": "Invalid or expired token",
    "registration_success": "Registration successful",
    "login_success": "Login successful",
    "logout_success": "Logout successful",
    "profile_updated": "Profile updated successfully",
}
