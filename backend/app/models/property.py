from datetime import datetime
from enum import Enum

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum as SQLEnum,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class PropertyType(str, Enum):
    APARTMENT = "apartment"
    HOUSE = "house"
    VILLA = "villa"
    PG = "pg"
    HOSTEL = "hostel"
    ROOM = "room"


class FurnishingStatus(str, Enum):
    FURNISHED = "furnished"
    SEMI_FURNISHED = "semi_furnished"
    UNFURNISHED = "unfurnished"


class Property(Base):
    __tablename__ = "properties"

    __table_args__ = (
        Index(
            "ix_properties_property_type",
            "property_type",
        ),
        Index(
            "ix_properties_monthly_rent",
            "monthly_rent",
        ),
        Index(
            "ix_properties_bedrooms",
            "bedrooms",
        ),
        Index(
            "ix_properties_furnishing_status",
            "furnishing_status",
        ),
        Index(
            "ix_properties_is_available",
            "is_available",
        ),
        Index(
            "ix_properties_created_at",
            "created_at",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    property_type: Mapped[PropertyType] = mapped_column(
        SQLEnum(PropertyType),
        nullable=False,
    )

    address: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    state: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    pincode: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    latitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    longitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    monthly_rent: Mapped[float] = mapped_column(
        nullable=False,
    )

    security_deposit: Mapped[float | None] = mapped_column(
        nullable=True,
    )

    bedrooms: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    bathrooms: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    furnishing_status: Mapped[FurnishingStatus | None] = mapped_column(
        SQLEnum(FurnishingStatus),
        nullable=True,
    )

    available_from: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    is_available: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    owner = relationship(
        "User",
        back_populates="properties",
    )

    favorites: Mapped[list["Favorite"]] = relationship(
        "Favorite",
        back_populates="property",
        cascade="all, delete-orphan",
    )

    images: Mapped[list["PropertyImage"]] = relationship(
        "PropertyImage",
        back_populates="property",
        cascade="all, delete-orphan",
        order_by="PropertyImage.display_order",
    )