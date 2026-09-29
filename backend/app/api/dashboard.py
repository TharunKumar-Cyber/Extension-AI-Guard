from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.dashboard_records import (
    AlertRecord,
    DetectionRecord,
    SecurityEventRecord,
)
from backend.app.models.dashboard_schemas import (
    DashboardAlert,
    DashboardDetection,
    DashboardSecurityEvent,
    DashboardSummary,
)
from backend.app.services.jwt_service import get_current_user_id

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"],
    dependencies=[Depends(get_current_user_id)],
)


@router.get("/summary", response_model=DashboardSummary)
def dashboard_summary(db: Session = Depends(get_db)):
    detection_count = db.query(func.count(DetectionRecord.id)).scalar() or 0
    malicious_count = (
        db.query(func.count(DetectionRecord.id))
        .filter(DetectionRecord.is_malicious.is_(True))
        .scalar()
        or 0
    )
    benign_count = detection_count - malicious_count
    alert_count = db.query(func.count(AlertRecord.id)).scalar() or 0
    event_count = db.query(func.count(SecurityEventRecord.id)).scalar() or 0
    latest = db.query(DetectionRecord).order_by(DetectionRecord.id.desc()).first()

    return DashboardSummary(
        detection_count=detection_count,
        malicious_count=malicious_count,
        benign_count=benign_count,
        alert_count=alert_count,
        event_count=event_count,
        latest_detection=latest,
    )


@router.get("/detections", response_model=list[DashboardDetection])
def dashboard_detections(db: Session = Depends(get_db)):
    return (
        db.query(DetectionRecord)
        .order_by(DetectionRecord.id.desc())
        .limit(100)
        .all()
    )


@router.get("/alerts", response_model=list[DashboardAlert])
def dashboard_alerts(db: Session = Depends(get_db)):
    return (
        db.query(AlertRecord)
        .order_by(AlertRecord.id.desc())
        .limit(100)
        .all()
    )


@router.get("/security-events", response_model=list[DashboardSecurityEvent])
def dashboard_security_events(db: Session = Depends(get_db)):
    return (
        db.query(SecurityEventRecord)
        .order_by(SecurityEventRecord.id.desc())
        .limit(100)
        .all()
    )
