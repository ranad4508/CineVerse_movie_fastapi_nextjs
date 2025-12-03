from sqlalchemy import Column, Integer, Boolean
from .base import BaseModel


class Watchlist(BaseModel):
    __tablename__ = "watchlist"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    movie_id = Column(Integer, nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
