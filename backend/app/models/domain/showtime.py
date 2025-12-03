from sqlalchemy import Column, Integer, DateTime, String, Float, Boolean
from .base import BaseModel


class Showtime(BaseModel):
    __tablename__ = "showtimes"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, nullable=False, index=True)
    screen_id = Column(Integer, nullable=False, index=True)
    cinema_id = Column(Integer, nullable=False, index=True)
    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime, nullable=False)
    base_price = Column(Float, nullable=False)
    available_seats = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
