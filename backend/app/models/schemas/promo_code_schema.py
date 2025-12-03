from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class DiscountType(str, Enum):
    PERCENTAGE = "percentage"
    FIXED = "fixed"


class PromoCodeBase(BaseModel):
    code: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None
    discount_type: DiscountType
    discount_value: float = Field(..., gt=0)
    max_usage: Optional[int] = Field(None, gt=0)
    min_booking_amount: float = Field(default=0.0, ge=0)
    valid_from: datetime
    valid_until: datetime


class PromoCodeCreate(PromoCodeBase):
    pass


class PromoCodeUpdate(BaseModel):
    description: Optional[str] = None
    discount_value: Optional[float] = Field(None, gt=0)
    max_usage: Optional[int] = Field(None, gt=0)
    valid_until: Optional[datetime] = None


class PromoCodeResponse(PromoCodeBase):
    id: int
    usage_count: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
