from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.properties import router as properties_router


router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "ApnaGhar API",
    }


router.include_router(auth_router)
router.include_router(properties_router)