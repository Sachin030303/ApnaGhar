from fastapi import APIRouter
from app.api.v1.favorites import router as favorites_router
from app.api.v1.auth import router as auth_router
from app.api.v1.properties import router as properties_router
from app.api.v1.property_images import router as property_images_router

router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "ApnaGhar API",
    }


router.include_router(favorites_router)
router.include_router(auth_router)
router.include_router(properties_router)
router.include_router(property_images_router)