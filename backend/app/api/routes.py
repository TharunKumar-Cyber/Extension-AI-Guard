from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.dashboard_records import (
    AlertRecord,
    DetectionRecord,
    NetworkRequestRecord,
    SecurityEventRecord,
)
from backend.app.services.alert import create_alert
from backend.app.services.security_event import create_security_event
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
def create_network_request(
    request: NetworkRequest,
    db: Session = Depends(get_db),
):
    result = analyze_request(request)
    alert = create_alert(result)

    event = create_security_event(
        event_type="network_request",
        source="extension",
        severity=alert.severity if alert else "low",
        description=result.explanation,
    )

    now = datetime.now(timezone.utc)
    db.add(
        NetworkRequestRecord(
            request_id=request.request_id,
            url=request.url,
            method=request.method,
            domain=request.domain,
            observed_at=request.timestamp,
            created_at=now,
        )
    )
    db.add(
        DetectionRecord(
            result_id=result.result_id,
            request_id=result.request_id,
            is_malicious=result.is_malicious,
            confidence=result.confidence,
            threat_type=result.threat_type,
            explanation=result.explanation,
            created_at=now,
        )
    )
    if alert:
        db.add(
            AlertRecord(
                alert_id=alert.alert_id,
                result_id=alert.result_id,
                severity=alert.severity,
                title=alert.title,
                message=alert.message,
                created_at=alert.created_at,
                acknowledged=alert.acknowledged,
            )
        )
    db.add(
        SecurityEventRecord(
            event_id=event.event_id,
            event_type=event.event_type,
            source=event.source,
            severity=event.severity,
            description=event.description,
            timestamp=event.timestamp,
        )
    )
    db.commit()

    return {
        "status": "analyzed",
        "request": request.model_dump(),
        "detection": result.model_dump(),
        "alert": alert.model_dump() if alert else None,
        "security_event": event.model_dump(),
    }
