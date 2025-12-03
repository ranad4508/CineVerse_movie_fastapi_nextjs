from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.movie_service import MovieService
from app.api.v1.dependencies import get_current_user, get_current_admin_user
from app.models.domain.user import User
from app.models.domain.movie import MovieStatus
from app.models.schemas.movie_schema import MovieCreate, MovieUpdate, MovieResponse

router = APIRouter(prefix="/movies", tags=["movies"])


@router.get("", response_model=list[MovieResponse])
def get_movies(
    status: MovieStatus = Query(None),
    genre: str = Query(None),
    search: str = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    movie_service = MovieService(db)
    
    if search:
        movies = movie_service.search_movies(search, skip, limit)
    elif status:
        movies = movie_service.get_movies_by_status(status, skip, limit)
    elif genre:
        movies = movie_service.search_by_genre(genre, skip, limit)
    else:
        movies = movie_service.get_active_movies(skip, limit)
    
    return movies


@router.get("/now-playing", response_model=list[MovieResponse])
def get_now_playing_movies(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    movie_service = MovieService(db)
    return movie_service.get_movies_by_status(MovieStatus.NOW_PLAYING, skip, limit)


@router.get("/coming-soon", response_model=list[MovieResponse])
def get_coming_soon_movies(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    movie_service = MovieService(db)
    return movie_service.get_movies_by_status(MovieStatus.COMING_SOON, skip, limit)


@router.get("/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie_service = MovieService(db)
    movie = movie_service.get_movie(movie_id)
    
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found"
        )
    
    return movie


@router.post("", response_model=MovieResponse, status_code=status.HTTP_201_CREATED)
def create_movie(
    movie_create: MovieCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    movie_service = MovieService(db)
    movie = movie_service.create_movie(movie_create)
    return movie


@router.put("/{movie_id}", response_model=MovieResponse)
def update_movie(
    movie_id: int,
    movie_update: MovieUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    movie_service = MovieService(db)
    movie = movie_service.update_movie(movie_id, movie_update)
    
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found"
        )
    
    return movie


@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(
    movie_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    movie_service = MovieService(db)
    
    if not movie_service.delete_movie(movie_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found"
        )
