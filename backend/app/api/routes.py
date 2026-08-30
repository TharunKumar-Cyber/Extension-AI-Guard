from fastapi import APIRouter

from backend.app.services.alert import create_alert
from backend.app.models.network_request import NetworkRequest
from backend.app.services.database import database_status
from backend.app.services.detection import analyze_request


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
    result = analyze_request(request)
    alert = create_alert(result)

    return {
        "status": "analyzed",
        "request": request.model_dump(),
        "detection": result.model_dump(),
        "alert": alert.model_dump() if alert else None,
    }