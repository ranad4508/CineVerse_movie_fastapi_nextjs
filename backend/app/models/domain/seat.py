from sqlalchemy import Column, Integer, String, Boolean, Enum as SQLEnum
from enum import Enum
from .base import BaseModel


class SeatCategory(str, Enum):
    STANDARD = "standard"
    GOLD = "gold"
    PLATINUM = "platinum"
    VIP = "vip"
    WHEELCHAIR = "wheelchair"


class SeatStatus(str, Enum):
    AVAILABLE = "available"
    BOOKED = "booked"
    RESERVED = "reserved"
    BLOCKED = "blocked"


class Seat(BaseModel):
    __tablename__ = "seats"

    id = Column(Integer, primary_key=True, index=True)
    screen_id = Column(Integer, nullable=False, index=True)
    row = Column(String(5), nullable=False)
    seat_number = Column(Integer, nullable=False)
    category = Column(SQLEnum(SeatCategory), default=SeatCategory.STANDARD, nullable=False)
    status = Column(SQLEnum(SeatStatus), default=SeatStatus.AVAILABLE, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
