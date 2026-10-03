
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.property import PropertyType, FurnishingStatus
from app.schemas.property import PropertyListResponse
from app.services.property_service import PropertyService

router = APIRouter(
    prefix="/search",
    tags=["Property Search"],
)


@router.get("/properties", response_model=PropertyListResponse)
def search_properties(
    city: str | None = Query(default=None, min_length=2),
    property_type: PropertyType | None = None,
    min_rent: float | None = Query(default=None, ge=0),
    max_rent: float | None = Query(default=None, ge=0),
    bedrooms: int | None = Query(default=None, ge=0),
    furnishing_status: FurnishingStatus | None = None,
    is_available: bool = True,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    if min_rent is not None and max_rent is not None:
        if min_rent > max_rent:
            raise HTTPException(
                status_code=422,
                detail="min_rent cannot be greater than max_rent",
            )

    properties, total = PropertyService.search_properties(
        db=db,
        city=city,
        property_type=property_type,
        min_rent=min_rent,
        max_rent=max_rent,
        bedrooms=bedrooms,
        furnishing_status=furnishing_status,
        is_available=is_available,
        page=page,
        page_size=page_size,
    )

    return PropertyListResponse(
        items=properties,
        total=total,
        page=page,
        page_size=page_size,
    )
