from unittest import result
from urllib import request

from fastapi import APIRouter, Depends

from backend.app.services.alert import create_alert
from backend.app.services.security_event import create_security_event
from backend.app.models.network_request import NetworkRequest
from backend.app.services.database import database_status
from backend.app.services.detection import analyze_request
from backend.app.services.jwt_service import get_current_user_id


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

    event = create_security_event(
        event_type="network_request",
        source="extension",
        severity=alert.severity if alert else "low",
        description=result.explanation,
    )

    return {
        "status": "analyzed",
        "request": request.model_dump(),
        "detection": result.model_dump(),
        "alert": alert.model_dump() if alert else None,
        "security_event": event.model_dump(),
    }


@router.get("/protected-test")
def protected_test(user_id: int = Depends(get_current_user_id)):
    return {
        "status": "authorized",
        "message": "JWT authentication is working",
        "user_id": user_id,
    }