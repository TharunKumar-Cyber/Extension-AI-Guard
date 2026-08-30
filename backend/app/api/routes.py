from fastapi import APIRouter

from backend.app.models.network_request import NetworkRequest
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


@router.post("/network-requests")
def create_network_request(request: NetworkRequest):
    return {
        "status": "received",
        "request": request.model_dump(),
    }