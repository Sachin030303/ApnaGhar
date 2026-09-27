from sqlalchemy.orm import Session

from app.models.property import Property
from app.repositories.property_repository import PropertyRepository
from app.schemas.property import PropertyCreate, PropertyUpdate


class PropertyService:

    @staticmethod
    def create_property(
        db: Session,
        property_data: PropertyCreate,
        owner_id: int,
    ) -> Property:

        data = property_data.model_dump()

        data["owner_id"] = owner_id

        return PropertyRepository.create(
            db=db,
            property_data=data,
        )

    @staticmethod
    def get_property(
        db: Session,
        property_id: int,
    ) -> Property | None:

        return PropertyRepository.get_by_id(
            db=db,
            property_id=property_id,
        )

    @staticmethod
    def get_properties(
        db: Session,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[Property], int]:

        if page < 1:
            page = 1

        if page_size < 1:
            page_size = 20

        if page_size > 100:
            page_size = 100

        skip = (page - 1) * page_size

        properties = PropertyRepository.get_all(
            db=db,
            skip=skip,
            limit=page_size,
        )

        total = PropertyRepository.count(db=db)

        return properties, total

    @staticmethod
    def update_property(
        db: Session,
        property_obj: Property,
        property_data: PropertyUpdate,
    ) -> Property:

        data = property_data.model_dump(
            exclude_unset=True
        )

        return PropertyRepository.update(
            db=db,
            property_obj=property_obj,
            property_data=data,
        )

    @staticmethod
    def delete_property(
        db: Session,
        property_obj: Property,
    ) -> None:

        PropertyRepository.delete(
            db=db,
            property_obj=property_obj,
        )