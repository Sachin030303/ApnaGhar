from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.models.user import User

from app.core.database import get_db
from app.schemas.property import (
    PropertyCreate,
    PropertyListResponse,
    PropertyResponse,
    PropertyUpdate,
)
from app.services.property_service import PropertyService


router = APIRouter(
    prefix="/properties",
    tags=["Properties"],
)


@router.post(
    "",
    response_model=PropertyResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_property(
    property_data: PropertyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return PropertyService.create_property(
        db=db,
        property_data=property_data,
        owner_id=current_user.id,
    )


@router.get(
    "",
    response_model=PropertyListResponse,
)
def get_properties(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    properties, total = PropertyService.get_properties(
        db=db,
        page=page,
        page_size=page_size,
    )

    return PropertyListResponse(
        items=properties,
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/{property_id}",
    response_model=PropertyResponse,
)
def get_property(
    property_id: int,
    db: Session = Depends(get_db),
):
    property_obj = PropertyService.get_property(
        db=db,
        property_id=property_id,
    )

    if property_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found",
        )

    return property_obj


@router.put(
    "/{property_id}",
    response_model=PropertyResponse,
)
def update_property(
    property_id: int,
    property_data: PropertyUpdate,
    db: Session = Depends(get_db),
):
    property_obj = PropertyService.get_property(
        db=db,
        property_id=property_id,
    )

    if property_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found",
        )

    return PropertyService.update_property(
        db=db,
        property_obj=property_obj,
        property_data=property_data,
    )


@router.delete(
    "/{property_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_property(
    property_id: int,
    db: Session = Depends(get_db),
):
    property_obj = PropertyService.get_property(
        db=db,
        property_id=property_id,
    )

    if property_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found",
        )

    PropertyService.delete_property(
        db=db,
        property_obj=property_obj,
    )

    return None