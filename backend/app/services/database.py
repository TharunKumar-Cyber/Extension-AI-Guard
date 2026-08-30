from backend.app.core.config import settings


def get_database_url() -> str:
    """Return the configured database connection URL."""
    return settings.database_url