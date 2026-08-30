from backend.app.core.database import get_database_url


def database_status() -> dict[str, str]:
    """Return the current database configuration status."""
    database_url = get_database_url()

    return {
        "configured": str(bool(database_url)),
        "status": "configured" if database_url else "not_configured",
    }