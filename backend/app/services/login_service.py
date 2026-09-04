from sqlalchemy.orm import Session

from backend.app.models.user import User
from backend.app.services.auth import verify_password


def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> User | None:
    """Authenticate a user by email and password."""

    user = db.query(User).filter(User.email == email).first()

    if user is None:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user
