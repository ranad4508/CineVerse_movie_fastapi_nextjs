from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.domain.booking import Booking, Ticket, BookingStatus, PaymentStatus
from app.models.schemas.booking_schema import BookingCreate, BookingUpdate
from app.repositories.booking_repository import BookingRepository, TicketRepository
from app.services.seat_service import SeatService
from app.models.domain.seat import SeatStatus
from datetime import datetime


class BookingService:
    def __init__(self, db: Session):
        self.repository = BookingRepository(db)
        self.ticket_repository = TicketRepository(db)
        self.seat_service = SeatService(db)

    def create_booking(self, user_id: int, booking_create: BookingCreate) -> Booking:
        booking = Booking(
            user_id=user_id,
            showtime_id=booking_create.showtime_id,
            total_price=booking_create.total_price,
            promo_code_id=booking_create.promo_code_id
        )
        created_booking = self.repository.create(booking)
        
        for ticket_data in booking_create.tickets:
            ticket = Ticket(
                booking_id=created_booking.id,
                seat_id=ticket_data.seat_id,
                ticket_category=ticket_data.ticket_category,
                price=ticket_data.price
            )
            self.ticket_repository.create(ticket)
            self.seat_service.update_seat_status(ticket_data.seat_id, SeatStatus.BOOKED)
        
        return created_booking

    def get_booking(self, booking_id: int) -> Optional[Booking]:
        return self.repository.get_by_id(booking_id)

    def get_all_bookings(self, skip: int = 0, limit: int = 100) -> List[Booking]:
        return self.repository.get_all(skip, limit)

    def get_user_bookings(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Booking]:
        return self.repository.get_by_user(user_id, skip, limit)

    def get_showtime_bookings(self, showtime_id: int, skip: int = 0, limit: int = 100) -> List[Booking]:
        return self.repository.get_by_showtime(showtime_id, skip, limit)

    def get_bookings_by_status(self, status: BookingStatus, skip: int = 0, limit: int = 100) -> List[Booking]:
        return self.repository.get_by_status(status, skip, limit)

    def update_booking_status(self, booking_id: int, status: BookingStatus) -> Optional[Booking]:
        return self.repository.update(booking_id, {"status": status})

    def update_payment_status(self, booking_id: int, payment_status: PaymentStatus, 
                            stripe_payment_id: str = None) -> Optional[Booking]:
        update_data = {"payment_status": payment_status}
        if stripe_payment_id:
            update_data["stripe_payment_id"] = stripe_payment_id
        return self.repository.update(booking_id, update_data)

    def update_booking(self, booking_id: int, booking_update: BookingUpdate) -> Optional[Booking]:
        update_data = booking_update.model_dump(exclude_unset=True)
        if update_data:
            return self.repository.update(booking_id, update_data)
        return self.get_booking(booking_id)

    def cancel_booking(self, booking_id: int) -> Optional[Booking]:
        booking = self.get_booking(booking_id)
        if booking:
            tickets = self.ticket_repository.get_by_booking(booking_id)
            for ticket in tickets:
                self.seat_service.update_seat_status(ticket.seat_id, SeatStatus.AVAILABLE)
            
            return self.repository.update(booking_id, {"status": BookingStatus.CANCELLED})
        return None

    def delete_booking(self, booking_id: int) -> bool:
        booking = self.get_booking(booking_id)
        if booking:
            self.cancel_booking(booking_id)
        return self.repository.delete(booking_id)


class TicketService:
    def __init__(self, db: Session):
        self.repository = TicketRepository(db)

    def get_ticket(self, ticket_id: int) -> Optional[Ticket]:
        return self.repository.get_by_id(ticket_id)

    def get_booking_tickets(self, booking_id: int) -> List[Ticket]:
        return self.repository.get_by_booking(booking_id)

    def mark_ticket_used(self, ticket_id: int) -> Optional[Ticket]:
        return self.repository.update(ticket_id, {"is_used": True})

    def get_all_tickets(self, skip: int = 0, limit: int = 100) -> List[Ticket]:
        return self.repository.get_all(skip, limit)
