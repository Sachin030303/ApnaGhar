from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.property import Property


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
    def count(
        db: Session,
    ) -> int:
        from sqlalchemy import func

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