from sqlalchemy import select, func, asc, desc
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
        latitude: float | None = None,
        longitude: float | None = None,
        radius_km: float | None = None,
        skip: int = 0,
        limit: int = 20,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> tuple[list[Property], int]:

        statement = select(Property)

        count_statement = select(
            func.count()
        ).select_from(Property)

        filters = []

        # -----------------------------------------
        # CITY FILTER
        # -----------------------------------------

        if city:
            filters.append(
                Property.city.ilike(
                    f"%{city.strip()}%"
                )
            )

        # -----------------------------------------
        # PROPERTY TYPE FILTER
        # -----------------------------------------

        if property_type is not None:
            filters.append(
                Property.property_type == property_type
            )

        # -----------------------------------------
        # MIN RENT FILTER
        # -----------------------------------------

        if min_rent is not None:
            filters.append(
                Property.monthly_rent >= min_rent
            )

        # -----------------------------------------
        # MAX RENT FILTER
        # -----------------------------------------

        if max_rent is not None:
            filters.append(
                Property.monthly_rent <= max_rent
            )

        # -----------------------------------------
        # BEDROOM FILTER
        # -----------------------------------------

        if bedrooms is not None:
            filters.append(
                Property.bedrooms == bedrooms
            )

        # -----------------------------------------
        # FURNISHING FILTER
        # -----------------------------------------

        if furnishing_status is not None:
            filters.append(
                Property.furnishing_status
                == furnishing_status
            )

        # -----------------------------------------
        # AVAILABILITY FILTER
        # -----------------------------------------

        if is_available is not None:
            filters.append(
                Property.is_available
                == is_available
            )

        # -----------------------------------------
        # LOCATION / RADIUS SEARCH
        # -----------------------------------------

        if (
            latitude is not None
            and longitude is not None
            and radius_km is not None
        ):

            # Haversine formula
            #
            # Earth radius = 6371 km
            #
            # distance =
            # 6371 * acos(
            #   cos(lat1)
            #   * cos(lat2)
            #   * cos(long2 - long1)
            #   + sin(lat1)
            #   * sin(lat2)
            # )

            distance = (
                6371
                * func.acos(
                    func.cos(
                        func.radians(latitude)
                    )
                    * func.cos(
                        func.radians(
                            Property.latitude
                        )
                    )
                    * func.cos(
                        func.radians(
                            Property.longitude
                        )
                        - func.radians(longitude)
                    )
                    + func.sin(
                        func.radians(latitude)
                    )
                    * func.sin(
                        func.radians(
                            Property.latitude
                        )
                    )
                )
            )

            filters.append(
                Property.latitude.is_not(None)
            )

            filters.append(
                Property.longitude.is_not(None)
            )

            filters.append(
                distance <= radius_km
            )

        # -----------------------------------------
        # APPLY FILTERS
        # -----------------------------------------

        if filters:

            statement = statement.where(
                *filters
            )

            count_statement = (
                count_statement.where(
                    *filters
                )
            )

        # -----------------------------------------
        # SORTING
        # -----------------------------------------

        sort_columns = {
            "monthly_rent": Property.monthly_rent,
            "created_at": Property.created_at,
        }

        column = sort_columns[sort_by]

        ordering = (
            asc(column)
            if sort_order == "asc"
            else desc(column)
        )

        statement = (
            statement
            .order_by(
                ordering,
                Property.id.desc()
            )
            .offset(skip)
            .limit(limit)
        )

        # -----------------------------------------
        # EXECUTE QUERY
        # -----------------------------------------

        properties = list(
            db.scalars(statement).all()
        )

        total = (
            db.scalar(count_statement)
            or 0
        )

        return properties, total