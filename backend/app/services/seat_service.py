from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.domain.seat import Seat, SeatStatus, SeatCategory
from app.models.schemas.seat_schema import SeatCreate, SeatUpdate
from app.repositories.seat_repository import SeatRepository


class SeatService:
    def __init__(self, db: Session):
        self.repository = SeatRepository(db)

    def create_seat(self, seat_create: SeatCreate) -> Seat:
        seat = Seat(
            screen_id=seat_create.screen_id,
            row=seat_create.row,
            seat_number=seat_create.seat_number,
            category=seat_create.category,
            status=seat_create.status
        )
        return self.repository.create(seat)

    def get_seat(self, seat_id: int) -> Optional[Seat]:
        return self.repository.get_by_id(seat_id)

    def get_all_seats(self, skip: int = 0, limit: int = 100) -> List[Seat]:
        return self.repository.get_all(skip, limit)

    def get_seats_by_screen(self, screen_id: int, skip: int = 0, limit: int = 100) -> List[Seat]:
        return self.repository.get_by_screen(screen_id, skip, limit)

    def get_available_seats(self, screen_id: int) -> List[Seat]:
        return self.repository.get_available_seats(screen_id)

    def get_booked_seats(self, screen_id: int) -> List[Seat]:
        return self.repository.get_booked_seats(screen_id)

    def get_seats_by_category(self, screen_id: int, category: SeatCategory) -> List[Seat]:
        return self.repository.get_seats_by_category(screen_id, category)

    def update_seat_status(self, seat_id: int, status: SeatStatus) -> Optional[Seat]:
        return self.repository.update(seat_id, {"status": status})

    def update_seat(self, seat_id: int, seat_update: SeatUpdate) -> Optional[Seat]:
        update_data = seat_update.model_dump(exclude_unset=True)
        if update_data:
            return self.repository.update(seat_id, update_data)
        return self.get_seat(seat_id)

    def delete_seat(self, seat_id: int) -> bool:
        return self.repository.delete(seat_id)

    def bulk_create_seats(self, screen_id: int, rows: List[str], seats_per_row: int, 
                         categories: dict = None) -> List[Seat]:
        seats = []
        for row in rows:
            for seat_num in range(1, seats_per_row + 1):
                category = categories.get(row, SeatCategory.STANDARD) if categories else SeatCategory.STANDARD
                seat = Seat(
                    screen_id=screen_id,
                    row=row,
                    seat_number=seat_num,
                    category=category
                )
                seats.append(seat)
        
        for seat in seats:
            self.repository.create(seat)
        
        return seats
