from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DashboardDetection(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    result_id: str
    request_id: str
    is_malicious: bool
    confidence: float
    threat_type: str
    explanation: str
    created_at: datetime


class DashboardAlert(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    alert_id: str
    result_id: str
    severity: str
    title: str
    message: str
    created_at: datetime
    acknowledged: bool


class DashboardSecurityEvent(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    event_id: str
    event_type: str
    source: str
    severity: str
    description: str
    timestamp: datetime


class DashboardSummary(BaseModel):
    detection_count: int
    malicious_count: int
    benign_count: int
    alert_count: int
    event_count: int
    latest_detection: DashboardDetection | None
