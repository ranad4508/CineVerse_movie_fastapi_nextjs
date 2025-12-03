# CineVerse Backend Setup

## Project Structure Created

The backend has been fully structured following FastAPI best practices with the following components:

### Core Modules

**`app/core/`**
- `config.py` - Configuration management with Pydantic Settings
- `security.py` - JWT token creation and verification
- `firebase.py` - Firebase authentication integration
- `logging.py` - Application logging configuration

### Database

**`app/db/`**
- `session.py` - SQLAlchemy database session management
- `migrations/` - Alembic migrations directory

### Domain Models

**`app/models/domain/`**
- `base.py` - Base model with timestamps
- `user.py` - User model with roles (admin/user)
- `movie.py` - Movie catalog model
- `cinema.py` - Cinema and Screen models
- `seat.py` - Seat model with categories and status
- `showtime.py` - Showtime model
- `booking.py` - Booking and Ticket models
- `review.py` - Movie review model
- `promo_code.py` - Discount code model
- `watchlist.py` - User watchlist model

### Pydantic Schemas

**`app/models/schemas/`**
- `user_schema.py` - User registration/login schemas
- `movie_schema.py` - Movie CRUD schemas
- `cinema_schema.py` - Cinema and Screen schemas
- `seat_schema.py` - Seat management schemas
- `showtime_schema.py` - Showtime schemas
- `booking_schema.py` - Booking and Ticket schemas
- `review_schema.py` - Review schemas
- `promo_code_schema.py` - Promo code schemas
- `watchlist_schema.py` - Watchlist schemas

### Repositories

**`app/repositories/`**
- `base.py` - Generic base repository with CRUD operations
- `user_repository.py` - User data access
- `movie_repository.py` - Movie queries with search/filter
- `cinema_repository.py` - Cinema and Screen queries
- `seat_repository.py` - Seat status and availability queries
- `showtime_repository.py` - Showtime queries and filtering
- `booking_repository.py` - Booking and Ticket queries

### Services

**`app/services/`**
- `user_service.py` - User management and authentication
- `movie_service.py` - Movie business logic
- `cinema_service.py` - Cinema management
- `seat_service.py` - Seat management and availability
- `showtime_service.py` - Showtime management
- `booking_service.py` - Booking and ticket operations

### API Routes

**`app/api/v1/routes/`**
- `auth.py` - Registration, login, Firebase verification
- `users.py` - User profile management (admin endpoints)
- `movies.py` - Movie catalog endpoints
- `cinemas.py` - Cinema management endpoints
- `showtimes.py` - Showtime endpoints
- `seats.py` - Seat management endpoints
- `bookings.py` - Booking and ticketing endpoints

**`app/api/`**
- `dependencies.py` - JWT dependency injection for auth
- `router.py` - Main API router combining all routes

### Main Entry

**`app/main.py`** - FastAPI app factory with:
- CORS middleware configuration
- Firebase initialization
- Database initialization
- Admin user creation on startup

## Authentication

### Features Implemented

✓ **User Registration & Login**
  - Email/password authentication
  - Firebase integration
  - JWT token generation
  - Firebase token verification

✓ **User Types**
  - Admin users (created on app startup)
  - Regular users
  - Role-based access control

✓ **Default Admin**
  - Email: `admin@example.com`
  - Password: `admin123`
  - Created automatically on first run (configured in .env)

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/verify-firebase-token` - Firebase token verification
- `POST /api/v1/auth/logout` - Logout

### Users
- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update own profile
- `GET /api/v1/users/{user_id}` - Get user details (admin)
- `GET /api/v1/users` - List all users (admin)
- `POST /api/v1/users/admin/create` - Create new admin (admin)
- `DELETE /api/v1/users/{user_id}` - Delete user (admin)

### Movies
- `GET /api/v1/movies` - List movies with filters
- `GET /api/v1/movies/now-playing` - Now playing movies
- `GET /api/v1/movies/coming-soon` - Coming soon movies
- `GET /api/v1/movies/{movie_id}` - Movie details
- `POST /api/v1/movies` - Create movie (admin)
- `PUT /api/v1/movies/{movie_id}` - Update movie (admin)
- `DELETE /api/v1/movies/{movie_id}` - Delete movie (admin)

### Cinemas
- `GET /api/v1/cinemas` - List cinemas
- `GET /api/v1/cinemas/{cinema_id}` - Cinema details
- `POST /api/v1/cinemas` - Create cinema (admin)
- `PUT /api/v1/cinemas/{cinema_id}` - Update cinema (admin)
- `DELETE /api/v1/cinemas/{cinema_id}` - Delete cinema (admin)
- `GET /api/v1/cinemas/{cinema_id}/screens` - Cinema screens
- `POST /api/v1/cinemas/{cinema_id}/screens` - Create screen (admin)

### Showtimes
- `GET /api/v1/showtimes` - List showtimes with filters
- `GET /api/v1/showtimes/{showtime_id}` - Showtime details
- `GET /api/v1/showtimes/movie/{movie_id}/upcoming` - Upcoming showtimes
- `POST /api/v1/showtimes` - Create showtime (admin)
- `PUT /api/v1/showtimes/{showtime_id}` - Update showtime (admin)
- `DELETE /api/v1/showtimes/{showtime_id}` - Delete showtime (admin)

### Seats
- `GET /api/v1/seats` - List seats with filters
- `GET /api/v1/seats/screen/{screen_id}/available` - Available seats
- `GET /api/v1/seats/screen/{screen_id}/booked` - Booked seats
- `GET /api/v1/seats/{seat_id}` - Seat details
- `POST /api/v1/seats` - Create seat (admin)
- `POST /api/v1/seats/screen/{screen_id}/bulk-create` - Bulk create seats (admin)
- `PUT /api/v1/seats/{seat_id}` - Update seat (admin)
- `DELETE /api/v1/seats/{seat_id}` - Delete seat (admin)

### Bookings
- `GET /api/v1/bookings/my-bookings` - User's bookings
- `GET /api/v1/bookings/{booking_id}` - Booking details
- `POST /api/v1/bookings` - Create booking
- `PUT /api/v1/bookings/{booking_id}` - Update booking
- `POST /api/v1/bookings/{booking_id}/cancel` - Cancel booking
- `DELETE /api/v1/bookings/{booking_id}` - Delete booking (admin)
- `GET /api/v1/bookings/{booking_id}/tickets` - Get booking tickets
- `PUT /api/v1/bookings/tickets/{ticket_id}/mark-used` - Mark ticket used (admin)

## Next Steps

1. **Database Migration**
   ```bash
   alembic init migrations
   alembic revision --autogenerate -m "Initial migration"
   alembic upgrade head
   ```

2. **Run the Application**
   ```bash
   uvicorn app.main:app --reload
   ```

3. **Access API Documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

4. **Features to Implement**
   - [ ] Email notifications with PDF tickets
   - [ ] Stripe payment integration
   - [ ] QR code generation for tickets
   - [ ] Review and rating system
   - [ ] Promo code validation
   - [ ] Watchlist functionality
   - [ ] Admin dashboard
