from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class CinemaBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    city: str = Field(..., min_length=1, max_length=100)
    location: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None


class CinemaCreate(CinemaBase):
    pass


class CinemaUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    city: Optional[str] = Field(None, min_length=1, max_length=100)
    location: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None


class CinemaResponse(CinemaBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ScreenBase(BaseModel):
    cinema_id: int
    screen_number: int = Field(..., gt=0)
    total_seats: int = Field(..., gt=0)
    screen_type: Optional[str] = None


class ScreenCreate(ScreenBase):
    pass


class ScreenUpdate(BaseModel):
    screen_number: Optional[int] = Field(None, gt=0)
    total_seats: Optional[int] = Field(None, gt=0)
    screen_type: Optional[str] = None


class ScreenResponse(ScreenBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
