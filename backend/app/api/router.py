from fastapi import APIRouter
from app.api.v1.routes import auth, users, movies, cinemas, showtimes, seats, bookings

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(movies.router)
api_router.include_router(cinemas.router)
api_router.include_router(showtimes.router)
api_router.include_router(seats.router)
api_router.include_router(bookings.router)
