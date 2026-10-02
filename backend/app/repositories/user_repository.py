from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:

    @staticmethod
    def get_by_id(
        db: Session,
        user_id: int,
    ) -> User | None:

        statement = select(User).where(
            User.id == user_id
        )

        return db.scalar(statement)

    @staticmethod
    def get_by_email(
        db: Session,
        email: str,
    ) -> User | None:

        statement = select(User).where(
            User.email == email
        )

        return db.scalar(statement)

    @staticmethod
    def create(
        db: Session,
        user_data: dict,
    ) -> User:

        user = User(**user_data)

        db.add(user)
        db.commit()
        db.refresh(user)

        return user