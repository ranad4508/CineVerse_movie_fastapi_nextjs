from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.domain.movie import Movie, MovieStatus
from app.models.schemas.movie_schema import MovieCreate, MovieUpdate
from app.repositories.movie_repository import MovieRepository


class MovieService:
    def __init__(self, db: Session):
        self.repository = MovieRepository(db)

    def create_movie(self, movie_create: MovieCreate) -> Movie:
        movie = Movie(
            title=movie_create.title,
            synopsis=movie_create.synopsis,
            cast=movie_create.cast,
            director=movie_create.director,
            genre=movie_create.genre,
            language=movie_create.language,
            duration=movie_create.duration,
            release_date=movie_create.release_date,
            poster_url=movie_create.poster_url,
            trailer_url=movie_create.trailer_url,
            age_restriction=movie_create.age_restriction,
            rating=movie_create.rating,
            status=movie_create.status
        )
        return self.repository.create(movie)

    def get_movie(self, movie_id: int) -> Optional[Movie]:
        return self.repository.get_by_id(movie_id)

    def get_all_movies(self, skip: int = 0, limit: int = 100) -> List[Movie]:
        return self.repository.get_all(skip, limit)

    def get_active_movies(self, skip: int = 0, limit: int = 100) -> List[Movie]:
        return self.repository.get_active_movies(skip, limit)

    def get_movies_by_status(self, status: MovieStatus, skip: int = 0, limit: int = 100) -> List[Movie]:
        return self.repository.get_by_status(status, skip, limit)

    def search_movies(self, query: str, skip: int = 0, limit: int = 100) -> List[Movie]:
        return self.repository.search_by_title(query, skip, limit)

    def search_by_genre(self, genre: str, skip: int = 0, limit: int = 100) -> List[Movie]:
        return self.repository.search_by_genre(genre, skip, limit)

    def update_movie(self, movie_id: int, movie_update: MovieUpdate) -> Optional[Movie]:
        movie = self.get_movie(movie_id)
        if not movie:
            return None

        update_data = {}
        if movie_update.title is not None:
            update_data["title"] = movie_update.title
        if movie_update.synopsis is not None:
            update_data["synopsis"] = movie_update.synopsis
        if movie_update.cast is not None:
            update_data["cast"] = movie_update.cast
        if movie_update.director is not None:
            update_data["director"] = movie_update.director
        if movie_update.genre is not None:
            update_data["genre"] = movie_update.genre
        if movie_update.language is not None:
            update_data["language"] = movie_update.language
        if movie_update.duration is not None:
            update_data["duration"] = movie_update.duration
        if movie_update.release_date is not None:
            update_data["release_date"] = movie_update.release_date
        if movie_update.poster_url is not None:
            update_data["poster_url"] = movie_update.poster_url
        if movie_update.trailer_url is not None:
            update_data["trailer_url"] = movie_update.trailer_url
        if movie_update.age_restriction is not None:
            update_data["age_restriction"] = movie_update.age_restriction
        if movie_update.rating is not None:
            update_data["rating"] = movie_update.rating
        if movie_update.status is not None:
            update_data["status"] = movie_update.status

        if update_data:
            return self.repository.update(movie_id, update_data)
        return movie

    def delete_movie(self, movie_id: int) -> bool:
        return self.repository.delete(movie_id)
