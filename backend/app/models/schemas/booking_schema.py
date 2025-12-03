from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class BookingStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class PaymentStatus(str, Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    REFUNDED = "refunded"


class TicketBase(BaseModel):
    booking_id: int
    seat_id: int
    ticket_category: str = Field(..., min_length=1, max_length=50)
    price: float = Field(..., gt=0)


class TicketCreate(TicketBase):
    pass


class TicketResponse(TicketBase):
    id: int
    qr_code: Optional[str] = None
    is_used: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class BookingBase(BaseModel):
    showtime_id: int
    total_price: float = Field(..., gt=0)
    promo_code_id: Optional[int] = None


class BookingCreate(BookingBase):
    tickets: List[TicketCreate]


class BookingUpdate(BaseModel):
    status: Optional[BookingStatus] = None
    payment_status: Optional[PaymentStatus] = None


class BookingResponse(BaseModel):
    id: int
    user_id: int
    showtime_id: int
    booking_date: datetime
    total_price: float
    status: BookingStatus
    payment_status: PaymentStatus
    promo_code_id: Optional[int] = None
    discount_amount: float
    stripe_payment_id: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
