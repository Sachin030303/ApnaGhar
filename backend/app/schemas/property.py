from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.property import (
    FurnishingStatus,
    PropertyType,
)


class PropertyBase(BaseModel):
    title: str = Field(min_length=5, max_length=200)
    description: str | None = None

    property_type: PropertyType

    address: str = Field(min_length=5, max_length=500)
    city: str = Field(min_length=2, max_length=100)
    state: str = Field(min_length=2, max_length=100)
    pincode: str = Field(min_length=4, max_length=10)

    latitude: float | None = Field(
        default=None,
        ge=-90,
        le=90,
    )

    longitude: float | None = Field(
        default=None,
        ge=-180,
        le=180,
    )

    monthly_rent: float = Field(gt=0)

    security_deposit: float | None = Field(
        default=None,
        ge=0,
    )

    bedrooms: int | None = Field(
        default=None,
        ge=0,
    )

    bathrooms: int | None = Field(
        default=None,
        ge=0,
    )

    furnishing_status: FurnishingStatus | None = None

    available_from: datetime | None = None

    is_available: bool = True


class PropertyCreate(PropertyBase):
    pass


class PropertyUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=5,
        max_length=200,
    )

    description: str | None = None

    property_type: PropertyType | None = None

    address: str | None = Field(
        default=None,
        min_length=5,
        max_length=500,
    )

    city: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    state: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    pincode: str | None = Field(
        default=None,
        min_length=4,
        max_length=10,
    )

    latitude: float | None = Field(
        default=None,
        ge=-90,
        le=90,
    )

    longitude: float | None = Field(
        default=None,
        ge=-180,
        le=180,
    )

    monthly_rent: float | None = Field(
        default=None,
        gt=0,
    )

    security_deposit: float | None = Field(
        default=None,
        ge=0,
    )

    bedrooms: int | None = Field(
        default=None,
        ge=0,
    )

    bathrooms: int | None = Field(
        default=None,
        ge=0,
    )

    furnishing_status: FurnishingStatus | None = None

    available_from: datetime | None = None

    is_available: bool | None = None


class PropertyResponse(PropertyBase):
    id: int
    owner_id: int

    is_verified: bool

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PropertyListResponse(BaseModel):
    items: list[PropertyResponse]
    total: int
    page: int
    page_size: int