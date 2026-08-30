from datetime import datetime, timezone

from backend.app.models.security_event import SecurityEvent


def create_security_event(
    event_type: str,
    source: str,
    description: str,
    severity: str = "low",
) -> SecurityEvent:
    """Create a security event with the current UTC timestamp."""

    return SecurityEvent(
        event_id=f"event-{datetime.now(timezone.utc).timestamp()}",
        event_type=event_type,
        source=source,
        severity=severity,
        description=description,
        timestamp=datetime.now(timezone.utc),
    )