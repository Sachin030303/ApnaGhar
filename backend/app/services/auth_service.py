from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, RegisterRequest


class AuthService:

    @staticmethod
    def register(
        db: Session,
        data: RegisterRequest,
    ) -> User:

        existing_user = UserRepository.get_by_email(
            db=db,
            email=data.email,
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        user_data = {
            "email": data.email,
            "password_hash": hash_password(data.password),
            "full_name": data.full_name,
            "role": data.role,
        }

        return UserRepository.create(
            db=db,
            user_data=user_data,
        )

    @staticmethod
    def login(
        db: Session,
        data: LoginRequest,
    ) -> tuple[User, str]:

        user = UserRepository.get_by_email(
            db=db,
            email=data.email,
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not verify_password(
            data.password,
            user.password_hash,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive",
            )

        access_token = create_access_token(
            data={
                "sub": str(user.id),
            }
        )

        return user, access_token