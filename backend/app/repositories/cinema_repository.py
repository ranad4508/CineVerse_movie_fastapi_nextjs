from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.domain.cinema import Cinema, Screen
from app.repositories.base import BaseRepository


class CinemaRepository(BaseRepository[Cinema]):
    def __init__(self, db: Session):
        super().__init__(Cinema, db)

    def get_by_city(self, city: str, skip: int = 0, limit: int = 100) -> List[Cinema]:
        return self.db.query(Cinema).filter(Cinema.city == city).offset(skip).limit(limit).all()

    def get_active_cinemas(self, skip: int = 0, limit: int = 100) -> List[Cinema]:
        return self.db.query(Cinema).filter(Cinema.is_active == True).offset(skip).limit(limit).all()


class ScreenRepository(BaseRepository[Screen]):
    def __init__(self, db: Session):
        super().__init__(Screen, db)

    def get_by_cinema(self, cinema_id: int, skip: int = 0, limit: int = 100) -> List[Screen]:
        return self.db.query(Screen).filter(Screen.cinema_id == cinema_id).offset(skip).limit(limit).all()

    def get_active_screens(self, cinema_id: int, skip: int = 0, limit: int = 100) -> List[Screen]:
        return self.db.query(Screen).filter(
            Screen.cinema_id == cinema_id,
            Screen.is_active == True
        ).offset(skip).limit(limit).all()
