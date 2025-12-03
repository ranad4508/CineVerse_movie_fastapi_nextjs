from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.seat_service import SeatService
from app.api.v1.dependencies import get_current_user, get_current_admin_user
from app.models.domain.user import User
from app.models.domain.seat import SeatStatus, SeatCategory
from app.models.schemas.seat_schema import SeatCreate, SeatUpdate, SeatResponse

router = APIRouter(prefix="/seats", tags=["seats"])


@router.get("", response_model=list[SeatResponse])
def get_seats(
    screen_id: int = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    seat_service = SeatService(db)
    
    if screen_id:
        seats = seat_service.get_seats_by_screen(screen_id, skip, limit)
    else:
        seats = seat_service.get_all_seats(skip, limit)
    
    return seats


@router.get("/screen/{screen_id}/available", response_model=list[SeatResponse])
def get_available_seats(
    screen_id: int,
    db: Session = Depends(get_db)
):
    seat_service = SeatService(db)
    seats = seat_service.get_available_seats(screen_id)
    return seats


@router.get("/screen/{screen_id}/booked", response_model=list[SeatResponse])
def get_booked_seats(
    screen_id: int,
    db: Session = Depends(get_db)
):
    seat_service = SeatService(db)
    seats = seat_service.get_booked_seats(screen_id)
    return seats


@router.get("/{seat_id}", response_model=SeatResponse)
def get_seat(seat_id: int, db: Session = Depends(get_db)):
    seat_service = SeatService(db)
    seat = seat_service.get_seat(seat_id)
    
    if not seat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seat not found"
        )
    
    return seat


@router.post("", response_model=SeatResponse, status_code=status.HTTP_201_CREATED)
def create_seat(
    seat_create: SeatCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    seat_service = SeatService(db)
    seat = seat_service.create_seat(seat_create)
    return seat


@router.post("/screen/{screen_id}/bulk-create", response_model=list[SeatResponse], status_code=status.HTTP_201_CREATED)
def bulk_create_seats(
    screen_id: int,
    rows: list[str] = Query(...),
    seats_per_row: int = Query(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    seat_service = SeatService(db)
    seats = seat_service.bulk_create_seats(screen_id, rows, seats_per_row)
    return seats


@router.put("/{seat_id}", response_model=SeatResponse)
def update_seat(
    seat_id: int,
    seat_update: SeatUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    seat_service = SeatService(db)
    seat = seat_service.update_seat(seat_id, seat_update)
    
    if not seat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seat not found"
        )
    
    return seat


@router.put("/{seat_id}/status", response_model=SeatResponse)
def update_seat_status(
    seat_id: int,
    status: SeatStatus = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    seat_service = SeatService(db)
    seat = seat_service.update_seat_status(seat_id, status)
    
    if not seat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seat not found"
        )
    
    return seat


@router.delete("/{seat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_seat(
    seat_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    seat_service = SeatService(db)
    
    if not seat_service.delete_seat(seat_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seat not found"
        )
