from datetime import datetime
from pydantic import BaseModel, Field


class SecurityEvent(BaseModel):
    """Represent a security event detected by Extension AI Guard."""

    event_id: str = Field(..., description="Unique identifier for the security event")
    event_type: str = Field(..., description="Type of security event")
    source: str = Field(..., description="Source of the event")
    severity: str = Field(
    ...,
    pattern="^(low|medium|high|critical)$",
    description="Severity level of the event",
)
    description: str = Field(..., description="Human-readable event description")
    timestamp: datetime = Field(..., description="Time when the event occurred")