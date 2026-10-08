from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.favorite import Favorite


class FavoriteRepository:

    @staticmethod
    def get_by_user_and_property(
        db: Session,
        user_id: int,
        property_id: int,
    ) -> Favorite | None:

        statement = select(Favorite).where(
            Favorite.user_id == user_id,
            Favorite.property_id == property_id,
        )

        return db.scalar(statement)

    @staticmethod
    def create(
        db: Session,
        user_id: int,
        property_id: int,
    ) -> Favorite:

        favorite = Favorite(
            user_id=user_id,
            property_id=property_id,
        )

        db.add(favorite)
        db.commit()
        db.refresh(favorite)

        return favorite

    @staticmethod
    def delete(
        db: Session,
        favorite: Favorite,
    ) -> None:

        db.delete(favorite)
        db.commit()

    @staticmethod
    def get_user_favorites(
        db: Session,
        user_id: int,
    ) -> list[Favorite]:

        statement = (
            select(Favorite)
            .options(selectinload(Favorite.property))
            .where(Favorite.user_id == user_id)
            .order_by(Favorite.created_at.desc())
        )

        return list(db.scalars(statement).all())