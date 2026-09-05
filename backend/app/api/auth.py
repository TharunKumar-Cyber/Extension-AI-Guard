from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.auth import RegisterRequest
from backend.app.models.login import LoginRequest
from backend.app.services.login_service import authenticate_user
from backend.app.services.user_service import register_user
from backend.app.services.jwt_service import create_access_token


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)


@router.post("/register")
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):
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


@router.post("/login")
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    user = authenticate_user(
        db=db,
        email=request.email,
        password=request.password,
    )

    if user is None:
        return {
            "status": "failed",
            "message": "Invalid email or password",
        }

    access_token = create_access_token(user.id)

    return {
        "status": "authenticated",
        "access_token": access_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active,
        },
    }