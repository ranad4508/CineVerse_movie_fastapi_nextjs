from pydantic import BaseModel
from datetime import datetime


class WatchlistBase(BaseModel):
    movie_id: int


class WatchlistCreate(WatchlistBase):
    pass


class WatchlistResponse(WatchlistBase):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
