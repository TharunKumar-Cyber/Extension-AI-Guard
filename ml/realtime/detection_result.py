from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class DetectionResult:
    event_id: str
    timestamp: str
    prediction: int | None
    label: str | None
    score: float | None
    model: str
    feature_schema: str
    status: str
    input_sequence: int | None = None
    preprocess_time_seconds: float | None = None
    inference_time_seconds: float | None = None
    total_time_seconds: float | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "timestamp": self.timestamp,
            "prediction": self.prediction,
            "label": self.label,
            "score": self.score,
            "model": self.model,
            "feature_schema": self.feature_schema,
            "status": self.status,
            "input_sequence": self.input_sequence,
            "preprocess_time_seconds": self.preprocess_time_seconds,
            "inference_time_seconds": self.inference_time_seconds,
            "total_time_seconds": self.total_time_seconds,
        }

    @staticmethod
    def utc_timestamp() -> str:
        return datetime.now(timezone.utc).isoformat()
