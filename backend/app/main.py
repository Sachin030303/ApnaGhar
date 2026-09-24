from fastapi import FastAPI

from app.api.v1.router import router
from app.core.config import settings


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Backend API for ApnaGhar03",
)


app.include_router(
    router,
    prefix="/api/v1",
)


@app.get("/")
def root():
    return {
        "message": "Welcome to ApnaGhar03 API",
        "version": settings.APP_VERSION,
    }