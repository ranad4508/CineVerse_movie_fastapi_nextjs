from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
import logging


logger = logging.getLogger(__name__)


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    
    for error in exc.errors():
        field_name = ".".join(str(x) for x in error["loc"][1:])
        error_message = error["msg"]
        error_type = error["type"]
        
        errors.append({
            "field": field_name,
            "message": error_message,
            "type": error_type
        })
    
    logger.warning(f"Validation error from {request.client.host}: {errors}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "message": "Request validation failed",
            "errors": errors,
            "code": 422
        }
    )


async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error from {request.client.host}: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "Internal server error",
            "error": "An unexpected error occurred. Please try again later.",
            "code": 500
        }
    )
