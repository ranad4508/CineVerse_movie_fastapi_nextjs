from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.domain.seat import Seat, SeatStatus, SeatCategory
from app.repositories.base import BaseRepository


class SeatRepository(BaseRepository[Seat]):
    def __init__(self, db: Session):
        super().__init__(Seat, db)

    def get_by_screen(self, screen_id: int, skip: int = 0, limit: int = 100) -> List[Seat]:
        return self.db.query(Seat).filter(Seat.screen_id == screen_id).offset(skip).limit(limit).all()

    def get_by_row_and_number(self, screen_id: int, row: str, seat_number: int) -> Optional[Seat]:
        return self.db.query(Seat).filter(
            Seat.screen_id == screen_id,
            Seat.row == row,
            Seat.seat_number == seat_number
        ).first()

    def get_available_seats(self, screen_id: int) -> List[Seat]:
        return self.db.query(Seat).filter(
            Seat.screen_id == screen_id,
            Seat.status == SeatStatus.AVAILABLE
        ).all()

    def get_booked_seats(self, screen_id: int) -> List[Seat]:
        return self.db.query(Seat).filter(
            Seat.screen_id == screen_id,
            Seat.status == SeatStatus.BOOKED
        ).all()

    def get_seats_by_category(self, screen_id: int, category: SeatCategory) -> List[Seat]:
        return self.db.query(Seat).filter(
            Seat.screen_id == screen_id,
            Seat.category == category
        ).all()
