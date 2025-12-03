from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Enum as SQLEnum
from enum import Enum
from datetime import datetime
from .base import BaseModel


class DiscountType(str, Enum):
    PERCENTAGE = "percentage"
    FIXED = "fixed"


class PromoCode(BaseModel):
    __tablename__ = "promo_codes"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(String(255), nullable=True)
    discount_type = Column(SQLEnum(DiscountType), nullable=False)
    discount_value = Column(Float, nullable=False)
    max_usage = Column(Integer, nullable=True)
    usage_count = Column(Integer, default=0, nullable=False)
    min_booking_amount = Column(Float, default=0.0, nullable=False)
    valid_from = Column(DateTime, nullable=False)
    valid_until = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
