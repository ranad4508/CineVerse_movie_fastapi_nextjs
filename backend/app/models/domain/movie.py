from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Enum as SQLEnum, Boolean, Date
from enum import Enum
from .base import BaseModel


class MovieStatus(str, Enum):
    NOW_PLAYING = "now_playing"
    COMING_SOON = "coming_soon"


class Movie(BaseModel):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    synopsis = Column(Text, nullable=True)
    cast = Column(String(500), nullable=True)
    director = Column(String(255), nullable=True)
    genre = Column(String(100), nullable=True, index=True)
    language = Column(String(50), nullable=True)
    duration = Column(Integer, nullable=False)
    release_date = Column(Date, nullable=False)
    poster_url = Column(String(500), nullable=True)
    trailer_url = Column(String(500), nullable=True)
    age_restriction = Column(String(10), nullable=True)
    rating = Column(Float, default=0.0, nullable=False)
    status = Column(SQLEnum(MovieStatus), default=MovieStatus.NOW_PLAYING, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
