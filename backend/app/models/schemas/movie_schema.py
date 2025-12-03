from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from enum import Enum


class MovieStatus(str, Enum):
    NOW_PLAYING = "now_playing"
    COMING_SOON = "coming_soon"


class MovieBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    synopsis: Optional[str] = None
    cast: Optional[str] = None
    director: Optional[str] = None
    genre: Optional[str] = None
    language: Optional[str] = None
    duration: int = Field(..., gt=0)
    release_date: date
    poster_url: Optional[str] = None
    trailer_url: Optional[str] = None
    age_restriction: Optional[str] = None
    rating: float = Field(default=0.0, ge=0.0, le=10.0)
    status: MovieStatus = MovieStatus.NOW_PLAYING


class MovieCreate(MovieBase):
    pass


class MovieUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    synopsis: Optional[str] = None
    cast: Optional[str] = None
    director: Optional[str] = None
    genre: Optional[str] = None
    language: Optional[str] = None
    duration: Optional[int] = Field(None, gt=0)
    release_date: Optional[date] = None
    poster_url: Optional[str] = None
    trailer_url: Optional[str] = None
    age_restriction: Optional[str] = None
    rating: Optional[float] = Field(None, ge=0.0, le=10.0)
    status: Optional[MovieStatus] = None


class MovieResponse(MovieBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
