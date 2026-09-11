from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fastapi import HTTPException, status

from backend.app.models.user import User
from backend.app.services.auth import hash_password


def register_user(
    db: Session,
    username: str,
    email: str,
    password: str,
) -> User:
    """Create and return a new user with a securely hashed password."""

    user = User(
        username=username,
        email=email,
        password_hash=hash_password(password),
    )

    db.add(user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or username already registered",
        )

    db.refresh(user)

    return user