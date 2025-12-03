from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ShowtimeBase(BaseModel):
    movie_id: int
    screen_id: int
    cinema_id: int
    start_time: datetime
    end_time: datetime
    base_price: float = Field(..., gt=0)
    available_seats: int = Field(..., ge=0)


class ShowtimeCreate(ShowtimeBase):
    pass


class ShowtimeUpdate(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    base_price: Optional[float] = Field(None, gt=0)
    available_seats: Optional[int] = Field(None, ge=0)


class ShowtimeResponse(ShowtimeBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
