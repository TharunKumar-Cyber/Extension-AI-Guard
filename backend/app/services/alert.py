from datetime import datetime, timezone

from backend.app.models.alert import Alert
from backend.app.models.detection_result import DetectionResult


def create_alert(result: DetectionResult) -> Alert | None:
    """Create an alert when a detection result is malicious."""

    if not result.is_malicious:
        return None

    return Alert(
        alert_id=f"alert-{result.result_id}",
        result_id=result.result_id,
        severity="high",
        title="Malicious Network Request Detected",
        message=result.explanation,
        created_at=datetime.now(timezone.utc),
    )