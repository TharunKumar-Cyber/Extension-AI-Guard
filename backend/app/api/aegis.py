from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.aegis_onboarding import AegisOnboarding
from backend.app.services.aegis_service import (
    explain_aegis_alert,
    get_aegis_response,
    get_aegis_knowledge,
    get_aegis_welcome,
)
from backend.app.services.jwt_service import get_current_user_id
from backend.app.models.auth import AegisMessageRequest

router = APIRouter(
    prefix="/api/aegis",
    tags=["Aegis"],
)


@router.get("/welcome")
def aegis_welcome():
    return get_aegis_welcome()


@router.get("/status")
def aegis_status(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    onboarding = (
        db.query(AegisOnboarding)
        .filter(AegisOnboarding.user_id == user_id)
        .first()
    )

    if onboarding is None:
        return {
            "user_id": user_id,
            "onboarding_exists": False,
            "started": False,
            "completed": False,
            "current_step": 1,
            "started_at": None,
            "completed_at": None,
        }

    return {
        "user_id": user_id,
        "onboarding_exists": True,
        "started": onboarding.started,
        "completed": onboarding.completed,
        "current_step": onboarding.current_step,
        "started_at": onboarding.started_at,
        "completed_at": onboarding.completed_at,
    }


@router.post("/onboarding/start")
def aegis_onboarding_start(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    onboarding = (
        db.query(AegisOnboarding)
        .filter(AegisOnboarding.user_id == user_id)
        .first()
    )

    if onboarding is not None:
        return {
            "message": "Onboarding already exists",
            "started": onboarding.started,
            "completed": onboarding.completed,
            "current_step": onboarding.current_step,
        }

    onboarding = AegisOnboarding(
        user_id=user_id,
        started=True,
        completed=False,
        current_step=1,
        started_at=datetime.now(timezone.utc),
    )

    db.add(onboarding)
    db.commit()
    db.refresh(onboarding)

    return {
        "message": "Aegis onboarding started",
        "started": onboarding.started,
        "completed": onboarding.completed,
        "current_step": onboarding.current_step,
        "started_at": onboarding.started_at,
    }
@router.post("/onboarding/step")
def aegis_onboarding_step(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    onboarding = (
        db.query(AegisOnboarding)
        .filter(AegisOnboarding.user_id == user_id)
        .first()
    )

    if onboarding is None:
        return {
            "message": "Onboarding has not been started",
            "started": False,
            "completed": False,
            "current_step": 1,
        }

    if onboarding.completed:
        return {
            "message": "Onboarding is already completed",
            "started": onboarding.started,
            "completed": onboarding.completed,
            "current_step": onboarding.current_step,
        }

    if onboarding.current_step >= 5:
        return {
            "message": "Onboarding is ready to be completed",
            "started": onboarding.started,
            "completed": onboarding.completed,
            "current_step": onboarding.current_step,
        }

    onboarding.current_step += 1

    db.commit()
    db.refresh(onboarding)

    return {
        "message": "Aegis onboarding step advanced",
        "started": onboarding.started,
        "completed": onboarding.completed,
        "current_step": onboarding.current_step,
    }
@router.post("/onboarding/complete")
def aegis_onboarding_complete(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    onboarding = (
        db.query(AegisOnboarding)
        .filter(AegisOnboarding.user_id == user_id)
        .first()
    )

    if onboarding is None:
        return {
            "message": "Onboarding has not been started",
            "started": False,
            "completed": False,
            "current_step": 1,
        }

    if onboarding.completed:
        return {
            "message": "Onboarding is already completed",
            "started": onboarding.started,
            "completed": onboarding.completed,
            "current_step": onboarding.current_step,
            "completed_at": onboarding.completed_at,
        }

    onboarding.completed = True
    onboarding.completed_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(onboarding)

    return {
        "message": "Aegis onboarding completed",
        "started": onboarding.started,
        "completed": onboarding.completed,
        "current_step": onboarding.current_step,
        "completed_at": onboarding.completed_at,
    }
@router.post("/message")
def aegis_message(
    request: AegisMessageRequest,
    user_id: int = Depends(get_current_user_id),
):
    return get_aegis_response(request.message)

@router.get("/knowledge")
def aegis_knowledge(
    user_id: int = Depends(get_current_user_id),
):
    return get_aegis_knowledge()

@router.get("/alerts/explain")
def aegis_alert_explain(
    severity: str,
    title: str,
    message: str,
    user_id: int = Depends(get_current_user_id),
):
    return explain_aegis_alert(
        severity=severity,
        title=title,
        message=message,
    )