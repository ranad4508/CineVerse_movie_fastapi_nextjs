from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.domain.movie import Movie, MovieStatus
from app.repositories.base import BaseRepository


class MovieRepository(BaseRepository[Movie]):
    def __init__(self, db: Session):
        super().__init__(Movie, db)

    def get_by_title(self, title: str) -> Optional[Movie]:
        return self.db.query(Movie).filter(Movie.title == title).first()

    def get_by_status(self, status: MovieStatus, skip: int = 0, limit: int = 100) -> List[Movie]:
        return self.db.query(Movie).filter(Movie.status == status).offset(skip).limit(limit).all()

    def search_by_genre(self, genre: str, skip: int = 0, limit: int = 100) -> List[Movie]:
        return self.db.query(Movie).filter(Movie.genre.ilike(f"%{genre}%")).offset(skip).limit(limit).all()

    def search_by_title(self, title: str, skip: int = 0, limit: int = 100) -> List[Movie]:
        return self.db.query(Movie).filter(Movie.title.ilike(f"%{title}%")).offset(skip).limit(limit).all()

    def get_active_movies(self, skip: int = 0, limit: int = 100) -> List[Movie]:
        return self.db.query(Movie).filter(Movie.is_active == True).offset(skip).limit(limit).all()
