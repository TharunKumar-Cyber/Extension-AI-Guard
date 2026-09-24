from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from ml.realtime.detection_engine import DetectionEngine
from ml.realtime.detection_result import DetectionResult


def detect_batch(
    observations: Iterable[dict[str, Any]],
    engine: DetectionEngine | None = None,
) -> list[DetectionResult]:
    """Process observations sequentially with one detection engine."""
    detection_engine = engine or DetectionEngine()

    results: list[DetectionResult] = []

    for observation in observations:
        results.append(detection_engine.detect(observation))

    return results