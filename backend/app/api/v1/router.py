from fastapi import APIRouter

from app.api.v1.properties import router as properties_router


router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "ApnaGhar API",
    }


router.include_router(properties_router)