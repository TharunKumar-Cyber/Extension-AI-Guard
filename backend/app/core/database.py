from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from backend.app.core.config import settings


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""


def get_database_url() -> str:
    """Return the configured database connection URL."""
    return settings.database_url


def get_db():
    """Provide a database session to API endpoints."""
    if not settings.database_url:
        raise RuntimeError("Database is not configured")

    engine = create_engine(settings.database_url)
    session_local = sessionmaker(bind=engine)

    db = session_local()

    try:
        yield db
    finally:
        db.close()
