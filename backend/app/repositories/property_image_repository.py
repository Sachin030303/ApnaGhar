from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.property_image import PropertyImage


class PropertyImageRepository:

    @staticmethod
    def create(
        db: Session,
        property_id: int,
        image_url: str,
        is_primary: bool = False,
        display_order: int = 0,
    ) -> PropertyImage:

        image = PropertyImage(
            property_id=property_id,
            image_url=image_url,
            is_primary=is_primary,
            display_order=display_order,
        )

        db.add(image)
        db.commit()
        db.refresh(image)

        return image

    @staticmethod
    def get_by_id(
        db: Session,
        image_id: int,
    ) -> PropertyImage | None:

        statement = select(PropertyImage).where(
            PropertyImage.id == image_id
        )

        return db.scalar(statement)

    @staticmethod
    def get_by_property(
        db: Session,
        property_id: int,
    ) -> list[PropertyImage]:

        statement = (
            select(PropertyImage)
            .where(PropertyImage.property_id == property_id)
            .order_by(
                PropertyImage.display_order.asc(),
                PropertyImage.created_at.asc(),
            )
        )

        return list(db.scalars(statement).all())

    @staticmethod
    def update(
        db: Session,
        image: PropertyImage,
        image_url: str | None = None,
        is_primary: bool | None = None,
        display_order: int | None = None,
    ) -> PropertyImage:

        if image_url is not None:
            image.image_url = image_url

        if is_primary is not None:
            image.is_primary = is_primary

        if display_order is not None:
            image.display_order = display_order

        db.commit()
        db.refresh(image)

        return image

    @staticmethod
    def delete(
        db: Session,
        image: PropertyImage,
    ) -> None:

        db.delete(image)
        db.commit()