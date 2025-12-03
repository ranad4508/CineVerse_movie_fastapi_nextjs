from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from datetime import timedelta
from app.db.session import get_db
from app.services.user_service import UserService
from app.core.security import create_access_token
from app.core.config import settings
from app.core.firebase import create_firebase_user, verify_firebase_token, get_firebase_user_by_email
from app.models.schemas.user_schema import UserCreate, UserResponse, UserBase
from app.models.domain.user import UserRole
from app.core.rate_limiter import get_rate_limit_key
from app.core.validators import PasswordValidator
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional

router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterRequest(UserBase):
    password: str = Field(..., min_length=8)
    
    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v):
        return PasswordValidator.validate_password(v)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


class FirebaseTokenRequest(BaseModel):
    id_token: str


@router.post("/register", response_model=TokenResponse)
def register(
    register_request: RegisterRequest,
    db: Session = Depends(get_db),
    rate_limit_key: str = Depends(get_rate_limit_key(calls=5, period=3600))
):
    user_service = UserService(db)
    
    try:
        firebase_uid = create_firebase_user(
            email=register_request.email,
            password=register_request.password,
            display_name=register_request.full_name
        )
        
        user_create = UserCreate(
            email=register_request.email,
            username=register_request.username,
            full_name=register_request.full_name,
            password=register_request.password
        )
        
        user = user_service.create_user(user_create, role=UserRole.USER)
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={
                "sub": user.id,
                "email": user.email,
                "username": user.username,
                "full_name": user.full_name,
                "role": user.role.value,
                "is_active": user.is_active
            },
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/login", response_model=TokenResponse)
def login(
    login_request: LoginRequest,
    db: Session = Depends(get_db),
    rate_limit_key: str = Depends(get_rate_limit_key(calls=10, period=900))
):
    user_service = UserService(db)
    
    firebase_user = get_firebase_user_by_email(login_request.email)
    if not firebase_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    user = user_service.get_user_by_email(login_request.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found in database"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.id,
            "email": user.email,
            "username": user.username,
            "full_name": user.full_name,
            "role": user.role.value,
            "is_active": user.is_active
        },
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@router.post("/verify-firebase-token", response_model=TokenResponse)
def verify_firebase_id_token(
    token_request: FirebaseTokenRequest,
    db: Session = Depends(get_db),
    rate_limit_key: str = Depends(get_rate_limit_key(calls=10, period=300))
):
    user_service = UserService(db)
    
    decoded_token = verify_firebase_token(token_request.id_token)
    if not decoded_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Firebase token"
        )
    
    email = decoded_token.get("email")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email not found in token"
        )
    
    user = user_service.get_user_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found. Please register first."
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.id,
            "email": user.email,
            "username": user.username,
            "full_name": user.full_name,
            "role": user.role.value,
            "is_active": user.is_active
        },
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@router.post("/logout")
def logout():
    return {"message": "Logged out successfully"}
