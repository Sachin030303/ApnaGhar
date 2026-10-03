
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.property import Property, PropertyType, FurnishingStatus


class PropertyRepository:

    @staticmethod
    def create(
        db: Session,
        property_data: dict,
    ) -> Property:
        property_obj = Property(**property_data)

        db.add(property_obj)
        db.commit()
        db.refresh(property_obj)

        return property_obj

    @staticmethod
    def get_by_id(
        db: Session,
        property_id: int,
    ) -> Property | None:
        statement = select(Property).where(
            Property.id == property_id
        )
        return db.scalar(statement)

    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Property]:
        statement = (
            select(Property)
            .offset(skip)
            .limit(limit)
            .order_by(Property.created_at.desc())
        )
        return list(db.scalars(statement).all())

    @staticmethod
    def count(db: Session) -> int:
        statement = select(func.count()).select_from(Property)
        return db.scalar(statement) or 0

    @staticmethod
    def update(
        db: Session,
        property_obj: Property,
        property_data: dict,
    ) -> Property:
        for field, value in property_data.items():
            setattr(property_obj, field, value)

        db.commit()
        db.refresh(property_obj)

        return property_obj

    @staticmethod
    def delete(
        db: Session,
        property_obj: Property,
    ) -> None:
        db.delete(property_obj)
        db.commit()

    @staticmethod
    def search_properties(
        db: Session,
        city: str | None = None,
        property_type: PropertyType | None = None,
        min_rent: float | None = None,
        max_rent: float | None = None,
        bedrooms: int | None = None,
        furnishing_status: FurnishingStatus | None = None,
        is_available: bool | None = True,
        skip: int = 0,
        limit: int = 20,
    ) -> tuple[list[Property], int]:

        statement = select(Property)
        count_statement = select(func.count()).select_from(Property)

        filters = []

        if city:
            filters.append(Property.city.ilike(f"%{city.strip()}%"))

        if property_type is not None:
            filters.append(Property.property_type == property_type)

        if min_rent is not None:
            filters.append(Property.monthly_rent >= min_rent)

        if max_rent is not None:
            filters.append(Property.monthly_rent <= max_rent)

        if bedrooms is not None:
            filters.append(Property.bedrooms == bedrooms)

        if furnishing_status is not None:
            filters.append(Property.furnishing_status == furnishing_status)

        if is_available is not None:
            filters.append(Property.is_available == is_available)

        if filters:
            statement = statement.where(*filters)
            count_statement = count_statement.where(*filters)

        statement = (
            statement
            .order_by(Property.created_at.desc())
            .offset(skip)
            .limit(limit)
        )

        properties = list(db.scalars(statement).all())
        total = db.scalar(count_statement) or 0

        return properties, total
