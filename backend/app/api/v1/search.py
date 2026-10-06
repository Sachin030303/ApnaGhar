from typing import Literal

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
)

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.property import (
    PropertyType,
    FurnishingStatus,
)

from app.schemas.property import (
    PropertySearchListResponse,
    PropertySearchResponse,
)

from app.services.property_service import (
    PropertyService,
)


router = APIRouter(
    prefix="/search",
    tags=["Property Search"],
)


@router.get(
    "/properties",
    response_model=PropertySearchListResponse,
)
def search_properties(

    # -----------------------------------------
    # BASIC SEARCH
    # -----------------------------------------

    city: str | None = Query(
        default=None,
        min_length=2,
    ),

    property_type: PropertyType | None = None,

    # -----------------------------------------
    # RENT
    # -----------------------------------------

    min_rent: float | None = Query(
        default=None,
        ge=0,
    ),

    max_rent: float | None = Query(
        default=None,
        ge=0,
    ),

    # -----------------------------------------
    # PROPERTY FILTERS
    # -----------------------------------------

    bedrooms: int | None = Query(
        default=None,
        ge=0,
    ),

    furnishing_status: (
        FurnishingStatus | None
    ) = None,

    is_available: bool = True,

    # -----------------------------------------
    # LOCATION
    # -----------------------------------------

    latitude: float | None = Query(
        default=None,
        ge=-90,
        le=90,
    ),

    longitude: float | None = Query(
        default=None,
        ge=-180,
        le=180,
    ),

    radius_km: float | None = Query(
        default=None,
        gt=0,
        le=100,
    ),

    # -----------------------------------------
    # PAGINATION
    # -----------------------------------------

    page: int = Query(
        default=1,
        ge=1,
    ),

    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
    ),

    # -----------------------------------------
    # SORTING
    # -----------------------------------------

    sort_by: Literal[
        "monthly_rent",
        "created_at",
        "distance",
    ] = Query(
        default="created_at",
    ),

    sort_order: Literal[
        "asc",
        "desc",
    ] = Query(
        default="desc",
    ),

    # -----------------------------------------
    # DATABASE
    # -----------------------------------------

    db: Session = Depends(get_db),
):

    # -----------------------------------------
    # RENT VALIDATION
    # -----------------------------------------

    if (
        min_rent is not None
        and max_rent is not None
        and min_rent > max_rent
    ):
        raise HTTPException(
            status_code=422,
            detail=(
                "min_rent cannot be greater "
                "than max_rent"
            ),
        )

    # -----------------------------------------
    # LOCATION VALIDATION
    # -----------------------------------------

    location_values = [
        latitude,
        longitude,
        radius_km,
    ]

    location_count = sum(
        value is not None
        for value in location_values
    )

    if (
        location_count > 0
        and location_count < 3
    ):
        raise HTTPException(
            status_code=422,
            detail=(
                "latitude, longitude and "
                "radius_km must all be provided "
                "for location search"
            ),
        )

    # -----------------------------------------
    # DISTANCE SORT VALIDATION
    # -----------------------------------------

    if sort_by == "distance":

        if (
            latitude is None
            or longitude is None
            or radius_km is None
        ):
            raise HTTPException(
                status_code=422,
                detail=(
                    "Distance sorting requires "
                    "latitude, longitude and "
                    "radius_km"
                ),
            )

    # -----------------------------------------
    # SEARCH
    # -----------------------------------------

    properties, total = (
        PropertyService.search_properties(
            db=db,
            city=city,
            property_type=property_type,
            min_rent=min_rent,
            max_rent=max_rent,
            bedrooms=bedrooms,
            furnishing_status=furnishing_status,
            is_available=is_available,
            latitude=latitude,
            longitude=longitude,
            radius_km=radius_km,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_order=sort_order,
        )
    )

    # -----------------------------------------
    # BUILD RESPONSE
    # -----------------------------------------

    items = []

    for property_obj, distance_km in properties:

        property_data = (
            PropertySearchResponse.model_validate(
                property_obj
            )
        )

        property_data = property_data.model_copy(
            update={
                "distance_km": (
                    round(distance_km, 2)
                    if distance_km is not None
                    else None
                )
            }
        )

        items.append(property_data)

    # -----------------------------------------
    # RESPONSE
    # -----------------------------------------

    return PropertySearchListResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
    )