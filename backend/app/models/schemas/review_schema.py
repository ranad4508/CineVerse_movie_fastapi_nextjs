from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from app.core.validators import FieldValidators


class ReviewBase(BaseModel):
    movie_id: int
    rating: float = Field(..., ge=0.0, le=5.0)
    comment: Optional[str] = None
    
    @field_validator('rating')
    @classmethod
    def validate_rating(cls, v):
        return FieldValidators.validate_review_rating(v)
    
    @field_validator('comment')
    @classmethod
    def validate_comment(cls, v):
        if v and len(v) > 0:
            if len(v) < 10:
                raise ValueError("Comment must be at least 10 characters long")
            if len(v) > 1000:
                raise ValueError("Comment cannot exceed 1000 characters")
            return v.strip()
        return v


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    rating: Optional[float] = Field(None, ge=0.0, le=5.0)
    comment: Optional[str] = None


class ReviewResponse(ReviewBase):
    id: int
    user_id: int
    is_approved: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
