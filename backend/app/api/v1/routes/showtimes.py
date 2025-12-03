from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime
from app.db.session import get_db
from app.services.showtime_service import ShowtimeService
from app.api.v1.dependencies import get_current_user, get_current_admin_user
from app.models.domain.user import User
from app.models.schemas.showtime_schema import ShowtimeCreate, ShowtimeUpdate, ShowtimeResponse

router = APIRouter(prefix="/showtimes", tags=["showtimes"])


@router.get("", response_model=list[ShowtimeResponse])
def get_showtimes(
    movie_id: int = Query(None),
    cinema_id: int = Query(None),
    screen_id: int = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    showtime_service = ShowtimeService(db)
    
    if movie_id:
        showtimes = showtime_service.get_showtimes_by_movie(movie_id, skip, limit)
    elif cinema_id:
        showtimes = showtime_service.get_showtimes_by_cinema(cinema_id, skip, limit)
    elif screen_id:
        showtimes = showtime_service.get_showtimes_by_screen(screen_id, skip, limit)
    else:
        showtimes = showtime_service.get_all_showtimes(skip, limit)
    
    return showtimes


@router.get("/movie/{movie_id}/upcoming", response_model=list[ShowtimeResponse])
def get_upcoming_showtimes(
    movie_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    showtime_service = ShowtimeService(db)
    showtimes = showtime_service.get_upcoming_showtimes(movie_id, skip, limit)
    return showtimes


@router.get("/{showtime_id}", response_model=ShowtimeResponse)
def get_showtime(showtime_id: int, db: Session = Depends(get_db)):
    showtime_service = ShowtimeService(db)
    showtime = showtime_service.get_showtime(showtime_id)
    
    if not showtime:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Showtime not found"
        )
    
    return showtime


@router.post("", response_model=ShowtimeResponse, status_code=status.HTTP_201_CREATED)
def create_showtime(
    showtime_create: ShowtimeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    showtime_service = ShowtimeService(db)
    showtime = showtime_service.create_showtime(showtime_create)
    return showtime


@router.put("/{showtime_id}", response_model=ShowtimeResponse)
def update_showtime(
    showtime_id: int,
    showtime_update: ShowtimeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    showtime_service = ShowtimeService(db)
    showtime = showtime_service.update_showtime(showtime_id, showtime_update)
    
    if not showtime:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Showtime not found"
        )
    
    return showtime


@router.delete("/{showtime_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_showtime(
    showtime_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    showtime_service = ShowtimeService(db)
    
    if not showtime_service.delete_showtime(showtime_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Showtime not found"
        )
