from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


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


class SeatBase(BaseModel):
    screen_id: int
    row: str = Field(..., min_length=1, max_length=5)
    seat_number: int = Field(..., gt=0)
    category: SeatCategory = SeatCategory.STANDARD
    status: SeatStatus = SeatStatus.AVAILABLE


class SeatCreate(SeatBase):
    pass


class SeatUpdate(BaseModel):
    category: Optional[SeatCategory] = None
    status: Optional[SeatStatus] = None


class SeatResponse(SeatBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
