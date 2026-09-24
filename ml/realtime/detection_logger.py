from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ml.realtime.detection_result import DetectionResult


PROJECT_ROOT = Path(__file__).resolve().parents[2]
LOG_DIR = PROJECT_ROOT / "ml" / "realtime" / "logs"
LOG_PATH = LOG_DIR / "detections.jsonl"


class DetectionLogger:
    """Append structured real-time detection results as JSON Lines."""

    def __init__(self, log_path: str | Path = LOG_PATH) -> None:
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, result: DetectionResult) -> None:
        """Persist one detection result as a single JSON object."""
        record: dict[str, Any] = result.to_dict()

        with self.log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    def read_all(self) -> list[dict[str, Any]]:
        """Read all persisted detection records."""
        if not self.log_path.exists():
            return []

        records: list[dict[str, Any]] = []

        with self.log_path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()

                if line:
                    records.append(json.loads(line))

        return records