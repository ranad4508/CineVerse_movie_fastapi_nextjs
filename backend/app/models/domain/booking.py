from sqlalchemy import Column, Integer, String, Float, DateTime, Enum as SQLEnum, Boolean
from enum import Enum
from datetime import datetime
from .base import BaseModel


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


class Booking(BaseModel):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    showtime_id = Column(Integer, nullable=False, index=True)
    booking_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(SQLEnum(BookingStatus), default=BookingStatus.PENDING, nullable=False)
    payment_status = Column(SQLEnum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False)
    promo_code_id = Column(Integer, nullable=True)
    discount_amount = Column(Float, default=0.0, nullable=False)
    stripe_payment_id = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)


class Ticket(BaseModel):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, nullable=False, index=True)
    seat_id = Column(Integer, nullable=False, index=True)
    ticket_category = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    qr_code = Column(String(500), nullable=True)
    is_used = Column(Boolean, default=False, nullable=False)
