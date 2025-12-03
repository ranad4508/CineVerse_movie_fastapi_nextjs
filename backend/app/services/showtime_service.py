from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
from app.models.domain.showtime import Showtime
from app.models.schemas.showtime_schema import ShowtimeCreate, ShowtimeUpdate
from app.repositories.showtime_repository import ShowtimeRepository


class ShowtimeService:
    def __init__(self, db: Session):
        self.repository = ShowtimeRepository(db)

    def create_showtime(self, showtime_create: ShowtimeCreate) -> Showtime:
        showtime = Showtime(
            movie_id=showtime_create.movie_id,
            screen_id=showtime_create.screen_id,
            cinema_id=showtime_create.cinema_id,
            start_time=showtime_create.start_time,
            end_time=showtime_create.end_time,
            base_price=showtime_create.base_price,
            available_seats=showtime_create.available_seats
        )
        return self.repository.create(showtime)

    def get_showtime(self, showtime_id: int) -> Optional[Showtime]:
        return self.repository.get_by_id(showtime_id)

    def get_all_showtimes(self, skip: int = 0, limit: int = 100) -> List[Showtime]:
        return self.repository.get_all(skip, limit)

    def get_showtimes_by_movie(self, movie_id: int, skip: int = 0, limit: int = 100) -> List[Showtime]:
        return self.repository.get_by_movie(movie_id, skip, limit)

    def get_showtimes_by_cinema(self, cinema_id: int, skip: int = 0, limit: int = 100) -> List[Showtime]:
        return self.repository.get_by_cinema(cinema_id, skip, limit)

    def get_showtimes_by_screen(self, screen_id: int, skip: int = 0, limit: int = 100) -> List[Showtime]:
        return self.repository.get_by_screen(screen_id, skip, limit)

    def get_upcoming_showtimes(self, movie_id: int, skip: int = 0, limit: int = 100) -> List[Showtime]:
        return self.repository.get_upcoming_showtimes(movie_id, skip, limit)

    def get_showtimes_by_date_range(self, movie_id: int, cinema_id: int, 
                                    start_date: datetime, end_date: datetime) -> List[Showtime]:
        return self.repository.get_showtimes_by_date_range(movie_id, cinema_id, start_date, end_date)

    def update_showtime(self, showtime_id: int, showtime_update: ShowtimeUpdate) -> Optional[Showtime]:
        update_data = showtime_update.model_dump(exclude_unset=True)
        if update_data:
            return self.repository.update(showtime_id, update_data)
        return self.get_showtime(showtime_id)

    def delete_showtime(self, showtime_id: int) -> bool:
        return self.repository.delete(showtime_id)

    def update_available_seats(self, showtime_id: int, seats_count: int) -> Optional[Showtime]:
        showtime = self.get_showtime(showtime_id)
        if showtime:
            new_count = max(0, showtime.available_seats - seats_count)
            return self.repository.update(showtime_id, {"available_seats": new_count})
        return None
