from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.models.domain.showtime import Showtime
from app.repositories.base import BaseRepository


class ShowtimeRepository(BaseRepository[Showtime]):
    def __init__(self, db: Session):
        super().__init__(Showtime, db)

    def get_by_movie(self, movie_id: int, skip: int = 0, limit: int = 100) -> List[Showtime]:
        return self.db.query(Showtime).filter(
            Showtime.movie_id == movie_id
        ).offset(skip).limit(limit).all()

    def get_by_cinema(self, cinema_id: int, skip: int = 0, limit: int = 100) -> List[Showtime]:
        return self.db.query(Showtime).filter(
            Showtime.cinema_id == cinema_id
        ).offset(skip).limit(limit).all()

    def get_by_screen(self, screen_id: int, skip: int = 0, limit: int = 100) -> List[Showtime]:
        return self.db.query(Showtime).filter(
            Showtime.screen_id == screen_id
        ).offset(skip).limit(limit).all()

    def get_upcoming_showtimes(self, movie_id: int, skip: int = 0, limit: int = 100) -> List[Showtime]:
        return self.db.query(Showtime).filter(
            Showtime.movie_id == movie_id,
            Showtime.start_time >= datetime.utcnow()
        ).offset(skip).limit(limit).all()

    def get_showtimes_by_date_range(self, movie_id: int, cinema_id: int, 
                                    start_date: datetime, end_date: datetime) -> List[Showtime]:
        return self.db.query(Showtime).filter(
            Showtime.movie_id == movie_id,
            Showtime.cinema_id == cinema_id,
            Showtime.start_time.between(start_date, end_date)
        ).all()
