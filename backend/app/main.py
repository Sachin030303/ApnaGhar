
from fastapi import FastAPI
from sqlalchemy import text

from app.api.v1.router import router
from app.api.v1 import search
from app.core.config import settings
from app.core.database import engine

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Backend API for ApnaGhar",
)

# Register existing API routes
app.include_router(
    router,
    prefix="/api/v1",
)

# Register property search routes
app.include_router(
    search.router,
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

    except Exception:
        return {
            "status": "error",
            "database": "disconnected",
        }
