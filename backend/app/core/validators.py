from pydantic import BaseModel, field_validator, ValidationInfo
from typing import Optional
import re


class PasswordValidator:
    @staticmethod
    def validate_password(password: str) -> str:
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        if not re.search(r'[A-Z]', password):
            raise ValueError("Password must contain at least one uppercase letter")
        
        if not re.search(r'[a-z]', password):
            raise ValueError("Password must contain at least one lowercase letter")
        
        if not re.search(r'[0-9]', password):
            raise ValueError("Password must contain at least one digit")
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValueError("Password must contain at least one special character")
        
        return password


class UsernameValidator:
    @staticmethod
    def validate_username(username: str) -> str:
        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters long")
        
        if len(username) > 100:
            raise ValueError("Username cannot exceed 100 characters")
        
        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            raise ValueError("Username can only contain letters, numbers, underscores, and hyphens")
        
        return username


class EmailValidator:
    @staticmethod
    def validate_email(email: str) -> str:
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(email_pattern, email):
            raise ValueError("Invalid email format")
        
        if len(email) > 255:
            raise ValueError("Email cannot exceed 255 characters")
        
        return email.lower()


class PhoneValidator:
    @staticmethod
    def validate_phone(phone: str) -> str:
        phone_pattern = r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$'
        
        if not re.match(phone_pattern, phone):
            raise ValueError("Invalid phone number format")
        
        return phone


class URLValidator:
    @staticmethod
    def validate_url(url: str) -> str:
        url_pattern = r'^https?:\/\/.+'
        
        if not re.match(url_pattern, url):
            raise ValueError("Invalid URL format. Must start with http:// or https://")
        
        if len(url) > 2048:
            raise ValueError("URL cannot exceed 2048 characters")
        
        return url


class FieldValidators:
    @staticmethod
    def validate_positive_number(value: float) -> float:
        if value <= 0:
            raise ValueError("Value must be greater than 0")
        return value
    
    @staticmethod
    def validate_rating(value: float) -> float:
        if not (0 <= value <= 10):
            raise ValueError("Rating must be between 0 and 10")
        return value
    
    @staticmethod
    def validate_review_rating(value: float) -> float:
        if not (0 <= value <= 5):
            raise ValueError("Review rating must be between 0 and 5")
        return value
    
    @staticmethod
    def validate_discount_percent(value: float) -> float:
        if not (0 <= value <= 100):
            raise ValueError("Discount percentage must be between 0 and 100")
        return value
    
    @staticmethod
    def validate_string_length(value: str, min_length: int = 1, max_length: int = 255) -> str:
        if len(value) < min_length:
            raise ValueError(f"String must be at least {min_length} characters long")
        if len(value) > max_length:
            raise ValueError(f"String cannot exceed {max_length} characters")
        return value.strip()
    
    @staticmethod
    def validate_non_empty_string(value: str) -> str:
        if not value or not value.strip():
            raise ValueError("String cannot be empty")
        return value.strip()
