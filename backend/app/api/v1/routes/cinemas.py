from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.cinema_service import CinemaService, ScreenService
from app.api.v1.dependencies import get_current_user, get_current_admin_user
from app.models.domain.user import User
from app.models.schemas.cinema_schema import (
    CinemaCreate, CinemaUpdate, CinemaResponse,
    ScreenCreate, ScreenUpdate, ScreenResponse
)

router = APIRouter(prefix="/cinemas", tags=["cinemas"])


@router.get("", response_model=list[CinemaResponse])
def get_cinemas(
    city: str = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    cinema_service = CinemaService(db)
    
    if city:
        cinemas = cinema_service.get_cinemas_by_city(city, skip, limit)
    else:
        cinemas = cinema_service.get_active_cinemas(skip, limit)
    
    return cinemas


@router.get("/{cinema_id}", response_model=CinemaResponse)
def get_cinema(cinema_id: int, db: Session = Depends(get_db)):
    cinema_service = CinemaService(db)
    cinema = cinema_service.get_cinema(cinema_id)
    
    if not cinema:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cinema not found"
        )
    
    return cinema


@router.post("", response_model=CinemaResponse, status_code=status.HTTP_201_CREATED)
def create_cinema(
    cinema_create: CinemaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    cinema_service = CinemaService(db)
    cinema = cinema_service.create_cinema(cinema_create)
    return cinema


@router.put("/{cinema_id}", response_model=CinemaResponse)
def update_cinema(
    cinema_id: int,
    cinema_update: CinemaUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    cinema_service = CinemaService(db)
    cinema = cinema_service.update_cinema(cinema_id, cinema_update)
    
    if not cinema:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cinema not found"
        )
    
    return cinema


@router.delete("/{cinema_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cinema(
    cinema_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    cinema_service = CinemaService(db)
    
    if not cinema_service.delete_cinema(cinema_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cinema not found"
        )


@router.get("/{cinema_id}/screens", response_model=list[ScreenResponse])
def get_cinema_screens(
    cinema_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    screen_service = ScreenService(db)
    screens = screen_service.get_screens_by_cinema(cinema_id, skip, limit)
    return screens


@router.post("/{cinema_id}/screens", response_model=ScreenResponse, status_code=status.HTTP_201_CREATED)
def create_screen(
    cinema_id: int,
    screen_create: ScreenCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    if screen_create.cinema_id != cinema_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cinema ID mismatch"
        )
    
    screen_service = ScreenService(db)
    screen = screen_service.create_screen(screen_create)
    return screen


@router.get("/screens/{screen_id}", response_model=ScreenResponse)
def get_screen(screen_id: int, db: Session = Depends(get_db)):
    screen_service = ScreenService(db)
    screen = screen_service.get_screen(screen_id)
    
    if not screen:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Screen not found"
        )
    
    return screen


@router.put("/screens/{screen_id}", response_model=ScreenResponse)
def update_screen(
    screen_id: int,
    screen_update: ScreenUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    screen_service = ScreenService(db)
    screen = screen_service.update_screen(screen_id, screen_update)
    
    if not screen:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Screen not found"
        )
    
    return screen


@router.delete("/screens/{screen_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_screen(
    screen_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    screen_service = ScreenService(db)
    
    if not screen_service.delete_screen(screen_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Screen not found"
        )
