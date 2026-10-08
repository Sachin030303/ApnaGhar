from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.property_image import (
    PropertyImageCreate,
    PropertyImageResponse,
    PropertyImageUpdate,
)
from app.services.property_image_service import PropertyImageService


router = APIRouter(
    prefix="/property-images",
    tags=["Property Images"],
)


@router.post(
    "/{property_id}",
    response_model=PropertyImageResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_property_image(
    property_id: int,
    image_data: PropertyImageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        image = PropertyImageService.add_image(
            db=db,
            user_id=current_user.id,
            property_id=property_id,
            image_url=image_data.image_url,
            is_primary=image_data.is_primary,
            display_order=image_data.display_order,
        )

        return image

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )

    except PermissionError as error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(error),
        )


@router.get(
    "/{property_id}",
    response_model=list[PropertyImageResponse],
)
def get_property_images(
    property_id: int,
    db: Session = Depends(get_db),
):
    try:
        return PropertyImageService.get_property_images(
            db=db,
            property_id=property_id,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )


@router.put(
    "/image/{image_id}",
    response_model=PropertyImageResponse,
)
def update_property_image(
    image_id: int,
    image_data: PropertyImageUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        image = PropertyImageService.update_image(
            db=db,
            user_id=current_user.id,
            image_id=image_id,
            image_url=image_data.image_url,
            is_primary=image_data.is_primary,
            display_order=image_data.display_order,
        )

        return image

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )

    except PermissionError as error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(error),
        )


@router.delete(
    "/image/{image_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_property_image(
    image_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        PropertyImageService.delete_image(
            db=db,
            user_id=current_user.id,
            image_id=image_id,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )

    except PermissionError as error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(error),
        )

    return None