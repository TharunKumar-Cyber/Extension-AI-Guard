from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from backend.app.core.config import settings


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""


def get_database_url() -> str:
    """Return the configured database connection URL."""
    return settings.database_url


if settings.database_url:
    engine = create_engine(settings.database_url)
    SessionLocal = sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
    )
else:
    engine = None
    SessionLocal = None


def get_db():
    """Provide a database session to API endpoints."""
    if SessionLocal is None:
        raise RuntimeError("Database is not configured")

    db: Session = SessionLocal()

    try:
        yield db
    finally:
        db.close()
