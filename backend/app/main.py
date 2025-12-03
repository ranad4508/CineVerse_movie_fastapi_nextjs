from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import init_db, SessionLocal
from app.core.config import settings
from app.core.firebase import init_firebase
from app.services.user_service import UserService
from app.models.schemas.user_schema import UserCreate
from app.models.domain.user import UserRole
from app.api.router import api_router
from app.core.firebase import create_firebase_user


def init_admin_user():
    db = SessionLocal()
    try:
        user_service = UserService(db)
        
        admin_exists = user_service.get_user_by_email(settings.ADMIN_EMAIL)
        if not admin_exists:
            admin_username = settings.ADMIN_EMAIL.split("@")[0]
            
            try:
                create_firebase_user(
                    email=settings.ADMIN_EMAIL,
                    password=settings.DEFAULT_ADMIN_PASSWORD,
                    display_name="Admin"
                )
            except ValueError as e:
                print(f"Firebase user already exists: {e}")
            
            admin_user = UserCreate(
                email=settings.ADMIN_EMAIL,
                username=admin_username,
                password=settings.DEFAULT_ADMIN_PASSWORD,
                full_name="Admin"
            )
            user_service.create_user(admin_user, role=UserRole.ADMIN)
            print(f"Default admin user created: {settings.ADMIN_EMAIL}")
        else:
            print(f"Admin user already exists: {settings.ADMIN_EMAIL}")
    except Exception as e:
        print(f"Error initializing admin user: {e}")
    finally:
        db.close()


def create_app():
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        description="CineVerse - Movie Ticketing System API"
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.FRONTEND_URL, "http://localhost:3000", "http://localhost:8000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    init_firebase()
    init_db()
    init_admin_user()
    
    app.include_router(api_router)
    
    @app.get("/")
    def read_root():
        return {"message": "Welcome to CineVerse API", "version": settings.PROJECT_VERSION}

    @app.get("/health")
    def health_check():
        return {"status": "healthy"}
    
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
