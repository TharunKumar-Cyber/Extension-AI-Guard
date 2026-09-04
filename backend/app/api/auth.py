from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.auth import RegisterRequest
from backend.app.services.user_service import register_user


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)


@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    user = register_user(
        db=db,
        username=request.username,
        email=request.email,
        password=request.password,
    )

    return {
        "status": "registered",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active,
        },
    }
