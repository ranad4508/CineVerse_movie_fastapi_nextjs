from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum
from app.core.validators import PasswordValidator, UsernameValidator, FieldValidators


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    full_name: Optional[str] = Field(None, max_length=255)
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        return UsernameValidator.validate_username(v)
    
    @field_validator('full_name')
    @classmethod
    def validate_full_name(cls, v):
        if v and len(v) > 0:
            return FieldValidators.validate_string_length(v, min_length=1, max_length=255)
        return v


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    
    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v):
        return PasswordValidator.validate_password(v)


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=100)
    full_name: Optional[str] = Field(None, max_length=255)
    password: Optional[str] = Field(None, min_length=8)


class UserResponse(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    role: UserRole
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class UserDetailResponse(UserResponse):
    pass


class AdminCreateRequest(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    full_name: Optional[str] = None
    password: str = Field(..., min_length=8)
