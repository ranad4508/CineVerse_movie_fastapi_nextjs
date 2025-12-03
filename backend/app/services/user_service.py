from sqlalchemy.orm import Session
from typing import Optional
from app.models.domain.user import User, UserRole
from app.models.schemas.user_schema import UserCreate, UserUpdate
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password, verify_password


class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def create_user(self, user_create: UserCreate, role: UserRole = UserRole.USER) -> User:
        existing_email = self.repository.get_by_email(user_create.email)
        if existing_email:
            raise ValueError(f"Email {user_create.email} already registered")

        existing_username = self.repository.get_by_username(user_create.username)
        if existing_username:
            raise ValueError(f"Username {user_create.username} already taken")

        user = User(
            email=user_create.email,
            username=user_create.username,
            full_name=user_create.full_name,
            hashed_password=hash_password(user_create.password),
            role=role,
            is_active=True,
        )
        return self.repository.create(user)

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.repository.get_by_email(email)

    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.repository.get_by_username(username)

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.repository.get_by_id(user_id)

    def verify_password(self, user: User, password: str) -> bool:
        return verify_password(password, user.hashed_password)

    def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        user = self.get_user_by_id(user_id)
        if not user:
            return None

        update_data = {}
        
        if user_update.email and user_update.email != user.email:
            existing_email = self.repository.get_by_email(user_update.email)
            if existing_email:
                raise ValueError(f"Email {user_update.email} already in use")
            update_data["email"] = user_update.email

        if user_update.username and user_update.username != user.username:
            existing_username = self.repository.get_by_username(user_update.username)
            if existing_username:
                raise ValueError(f"Username {user_update.username} already taken")
            update_data["username"] = user_update.username

        if user_update.full_name is not None:
            update_data["full_name"] = user_update.full_name

        if user_update.password:
            update_data["hashed_password"] = hash_password(user_update.password)

        if update_data:
            return self.repository.update(user_id, update_data)
        
        return user

    def get_all_users(self, skip: int = 0, limit: int = 100):
        return self.repository.get_all(skip, limit)

    def delete_user(self, user_id: int) -> bool:
        return self.repository.delete(user_id)
