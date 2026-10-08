from sqlalchemy.orm import Session

from app.models.favorite import Favorite
from app.repositories.favorite_repository import (
    FavoriteRepository,
)
from app.repositories.property_repository import (
    PropertyRepository,
)


class FavoriteService:

    @staticmethod
    def add_favorite(
        db: Session,
        user_id: int,
        property_id: int,
    ) -> Favorite:

        # Check property exists
        property_obj = PropertyRepository.get_by_id(
            db=db,
            property_id=property_id,
        )

        if property_obj is None:
            raise ValueError(
                "Property not found"
            )

        # Check if already favorited
        existing = (
            FavoriteRepository
            .get_by_user_and_property(
                db=db,
                user_id=user_id,
                property_id=property_id,
            )
        )

        if existing is not None:
            raise ValueError(
                "Property is already in favorites"
            )

        return FavoriteRepository.create(
            db=db,
            user_id=user_id,
            property_id=property_id,
        )

    @staticmethod
    def remove_favorite(
        db: Session,
        user_id: int,
        property_id: int,
    ) -> None:

        favorite = (
            FavoriteRepository
            .get_by_user_and_property(
                db=db,
                user_id=user_id,
                property_id=property_id,
            )
        )

        if favorite is None:
            raise ValueError(
                "Property is not in favorites"
            )

        FavoriteRepository.delete(
            db=db,
            favorite=favorite,
        )

    @staticmethod
    def get_user_favorites(
        db: Session,
        user_id: int,
    ) -> list[Favorite]:

        return (
            FavoriteRepository
            .get_user_favorites(
                db=db,
                user_id=user_id,
            )
        )