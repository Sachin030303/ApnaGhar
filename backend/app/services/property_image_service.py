from sqlalchemy.orm import Session

from app.models.property_image import PropertyImage
from app.repositories.property_image_repository import PropertyImageRepository
from app.repositories.property_repository import PropertyRepository


class PropertyImageService:

    @staticmethod
    def add_image(
        db: Session,
        user_id: int,
        property_id: int,
        image_url: str,
        is_primary: bool = False,
        display_order: int = 0,
    ) -> PropertyImage:

        # Check that the property exists
        property_obj = PropertyRepository.get_by_id(
            db=db,
            property_id=property_id,
        )

        if property_obj is None:
            raise ValueError("Property not found")

        # Only the property owner can add images
        if property_obj.owner_id != user_id:
            raise PermissionError(
                "You are not the owner of this property"
            )

        # If this image is primary, remove primary status
        # from the property's existing images.
        if is_primary:
            existing_images = PropertyImageRepository.get_by_property(
                db=db,
                property_id=property_id,
            )

            for image in existing_images:
                image.is_primary = False

            db.commit()

        return PropertyImageRepository.create(
            db=db,
            property_id=property_id,
            image_url=image_url,
            is_primary=is_primary,
            display_order=display_order,
        )

    @staticmethod
    def get_property_images(
        db: Session,
        property_id: int,
    ) -> list[PropertyImage]:

        # Check that the property exists
        property_obj = PropertyRepository.get_by_id(
            db=db,
            property_id=property_id,
        )

        if property_obj is None:
            raise ValueError("Property not found")

        return PropertyImageRepository.get_by_property(
            db=db,
            property_id=property_id,
        )

    @staticmethod
    def update_image(
        db: Session,
        user_id: int,
        image_id: int,
        image_url: str | None = None,
        is_primary: bool | None = None,
        display_order: int | None = None,
    ) -> PropertyImage:

        image = PropertyImageRepository.get_by_id(
            db=db,
            image_id=image_id,
        )

        if image is None:
            raise ValueError("Image not found")

        # Find the property that owns this image
        property_obj = PropertyRepository.get_by_id(
            db=db,
            property_id=image.property_id,
        )

        if property_obj is None:
            raise ValueError("Property not found")

        # Only the property owner can update the image
        if property_obj.owner_id != user_id:
            raise PermissionError(
                "You are not the owner of this property"
            )

        # If making this image primary,
        # remove primary status from other images.
        if is_primary is True:
            existing_images = PropertyImageRepository.get_by_property(
                db=db,
                property_id=image.property_id,
            )

            for existing_image in existing_images:
                if existing_image.id != image.id:
                    existing_image.is_primary = False

            db.commit()

        return PropertyImageRepository.update(
            db=db,
            image=image,
            image_url=image_url,
            is_primary=is_primary,
            display_order=display_order,
        )

    @staticmethod
    def delete_image(
        db: Session,
        user_id: int,
        image_id: int,
    ) -> None:

        image = PropertyImageRepository.get_by_id(
            db=db,
            image_id=image_id,
        )

        if image is None:
            raise ValueError("Image not found")

        # Find the property that owns this image
        property_obj = PropertyRepository.get_by_id(
            db=db,
            property_id=image.property_id,
        )

        if property_obj is None:
            raise ValueError("Property not found")

        # Only the property owner can delete the image
        if property_obj.owner_id != user_id:
            raise PermissionError(
                "You are not the owner of this property"
            )

        PropertyImageRepository.delete(
            db=db,
            image=image,
        )