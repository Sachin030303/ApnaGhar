from fastapi import FastAPI

from app.api.v1.router import router
from app.core.config import settings

from sqlalchemy import text

from app.core.database import engine

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Backend API for ApnaGhar",
)


app.include_router(
    router,
    prefix="/api/v1",
)


@app.get("/")
def root():
    return {
        "message": "Welcome to ApnaGhar API",
        "version": settings.APP_VERSION,
    }


@app.get("/db-health")
def database_health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "ok",
            "database": "connected",
        }

    except Exception as e:
        return {
            "status": "error",
            "database": "disconnected",
            "detail": str(e),
        }