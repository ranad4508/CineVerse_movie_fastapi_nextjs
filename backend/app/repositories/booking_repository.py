from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.domain.booking import Booking, Ticket, BookingStatus
from app.repositories.base import BaseRepository


class BookingRepository(BaseRepository[Booking]):
    def __init__(self, db: Session):
        super().__init__(Booking, db)

    def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Booking]:
        return self.db.query(Booking).filter(
            Booking.user_id == user_id
        ).offset(skip).limit(limit).all()

    def get_by_showtime(self, showtime_id: int, skip: int = 0, limit: int = 100) -> List[Booking]:
        return self.db.query(Booking).filter(
            Booking.showtime_id == showtime_id
        ).offset(skip).limit(limit).all()

    def get_by_status(self, status: BookingStatus, skip: int = 0, limit: int = 100) -> List[Booking]:
        return self.db.query(Booking).filter(
            Booking.status == status
        ).offset(skip).limit(limit).all()

    def get_user_bookings_by_status(self, user_id: int, status: BookingStatus) -> List[Booking]:
        return self.db.query(Booking).filter(
            Booking.user_id == user_id,
            Booking.status == status
        ).all()


class TicketRepository(BaseRepository[Ticket]):
    def __init__(self, db: Session):
        super().__init__(Ticket, db)

    def get_by_booking(self, booking_id: int) -> List[Ticket]:
        return self.db.query(Ticket).filter(Ticket.booking_id == booking_id).all()

    def get_by_seat(self, seat_id: int) -> Optional[Ticket]:
        return self.db.query(Ticket).filter(Ticket.seat_id == seat_id).first()
