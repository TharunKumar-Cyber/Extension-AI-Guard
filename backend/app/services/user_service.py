from sqlalchemy.orm import Session

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
    db.commit()
    db.refresh(user)

    return user
