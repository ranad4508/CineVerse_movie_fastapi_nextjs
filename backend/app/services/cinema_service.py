from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.domain.cinema import Cinema, Screen
from app.models.schemas.cinema_schema import CinemaCreate, CinemaUpdate, ScreenCreate, ScreenUpdate
from app.repositories.cinema_repository import CinemaRepository, ScreenRepository


class CinemaService:
    def __init__(self, db: Session):
        self.repository = CinemaRepository(db)

    def create_cinema(self, cinema_create: CinemaCreate) -> Cinema:
        cinema = Cinema(
            name=cinema_create.name,
            city=cinema_create.city,
            location=cinema_create.location,
            phone=cinema_create.phone,
            email=cinema_create.email
        )
        return self.repository.create(cinema)

    def get_cinema(self, cinema_id: int) -> Optional[Cinema]:
        return self.repository.get_by_id(cinema_id)

    def get_all_cinemas(self, skip: int = 0, limit: int = 100) -> List[Cinema]:
        return self.repository.get_all(skip, limit)

    def get_active_cinemas(self, skip: int = 0, limit: int = 100) -> List[Cinema]:
        return self.repository.get_active_cinemas(skip, limit)

    def get_cinemas_by_city(self, city: str, skip: int = 0, limit: int = 100) -> List[Cinema]:
        return self.repository.get_by_city(city, skip, limit)

    def update_cinema(self, cinema_id: int, cinema_update: CinemaUpdate) -> Optional[Cinema]:
        update_data = cinema_update.model_dump(exclude_unset=True)
        if update_data:
            return self.repository.update(cinema_id, update_data)
        return self.get_cinema(cinema_id)

    def delete_cinema(self, cinema_id: int) -> bool:
        return self.repository.delete(cinema_id)


class ScreenService:
    def __init__(self, db: Session):
        self.repository = ScreenRepository(db)

    def create_screen(self, screen_create: ScreenCreate) -> Screen:
        screen = Screen(
            cinema_id=screen_create.cinema_id,
            screen_number=screen_create.screen_number,
            total_seats=screen_create.total_seats,
            screen_type=screen_create.screen_type
        )
        return self.repository.create(screen)

    def get_screen(self, screen_id: int) -> Optional[Screen]:
        return self.repository.get_by_id(screen_id)

    def get_all_screens(self, skip: int = 0, limit: int = 100) -> List[Screen]:
        return self.repository.get_all(skip, limit)

    def get_screens_by_cinema(self, cinema_id: int, skip: int = 0, limit: int = 100) -> List[Screen]:
        return self.repository.get_by_cinema(cinema_id, skip, limit)

    def get_active_screens(self, cinema_id: int, skip: int = 0, limit: int = 100) -> List[Screen]:
        return self.repository.get_active_screens(cinema_id, skip, limit)

    def update_screen(self, screen_id: int, screen_update: ScreenUpdate) -> Optional[Screen]:
        update_data = screen_update.model_dump(exclude_unset=True)
        if update_data:
            return self.repository.update(screen_id, update_data)
        return self.get_screen(screen_id)

    def delete_screen(self, screen_id: int) -> bool:
        return self.repository.delete(screen_id)
