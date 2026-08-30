from fastapi import APIRouter

from backend.app.services.database import database_status


router = APIRouter(
    prefix="/api",
    tags=["General"],
)


@router.get("/status")
def status():
    return {
        "status": "online",
        "service": "Extension AI Guard API",
    }


@router.get("/database-status")
def database_connection_status():
    return database_status()