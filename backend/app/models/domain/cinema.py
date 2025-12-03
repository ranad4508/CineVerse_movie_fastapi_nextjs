from sqlalchemy import Column, Integer, String, Text, Boolean
from .base import BaseModel


class Cinema(BaseModel):
    __tablename__ = "cinemas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    city = Column(String(100), nullable=False, index=True)
    location = Column(Text, nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)


class Screen(BaseModel):
    __tablename__ = "screens"

    id = Column(Integer, primary_key=True, index=True)
    cinema_id = Column(Integer, nullable=False, index=True)
    screen_number = Column(Integer, nullable=False)
    total_seats = Column(Integer, nullable=False)
    screen_type = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
