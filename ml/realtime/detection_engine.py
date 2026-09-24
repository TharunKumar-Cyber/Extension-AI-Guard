from __future__ import annotations

import time
import uuid
from typing import Any

import joblib
import pandas as pd

from ml.realtime.detection_logger import DetectionLogger
from ml.realtime.detection_result import DetectionResult
from ml.realtime.feature_adapter import adapt_observation
from ml.realtime.realtime_config import (
    DEFAULT_MODEL_NAME,
    FEATURE_SCHEMA_VERSION,
    LABEL_MAPPING,
    MODEL_PATHS,
    PREPROCESSOR_PATH,
)

MODEL_FEATURE_NAMES = [str(index) for index in range(8)]


class DetectionEngine:
    """Phase 18 real-time traffic classification engine."""

    def __init__(
        self,
        model_name: str = DEFAULT_MODEL_NAME,
        logger: DetectionLogger | None = None,
    ) -> None:
        if model_name not in MODEL_PATHS:
            raise ValueError(f"unsupported model: {model_name!r}")

        self.model_name = model_name
        self.preprocessor = joblib.load(PREPROCESSOR_PATH)
        self.model = joblib.load(MODEL_PATHS[model_name])
        self.logger = logger
        self.sequence = 0

    def detect(self, observation: dict[str, Any]) -> DetectionResult:
        """Validate, preprocess, classify, log, and return one detection result."""
        event_id = str(uuid.uuid4())
        self.sequence += 1
        total_start = time.perf_counter()

        try:
            adapted = adapt_observation(observation)

            preprocess_start = time.perf_counter()
            frame = pd.DataFrame([adapted])
            transformed = self.preprocessor.transform(frame)

            features = pd.DataFrame(
                transformed,
                columns=MODEL_FEATURE_NAMES,
            )

            preprocess_time = time.perf_counter() - preprocess_start

            inference_start = time.perf_counter()
            prediction = int(self.model.predict(features)[0])

            probabilities = (
                self.model.predict_proba(features)[0]
                if hasattr(self.model, "predict_proba")
                else None
            )

            inference_time = time.perf_counter() - inference_start

            if prediction not in LABEL_MAPPING:
                raise ValueError(f"invalid model prediction: {prediction}")

            score = (
                float(probabilities[prediction])
                if probabilities is not None
                else None
            )

            total_time = time.perf_counter() - total_start

            result = DetectionResult(
                event_id=event_id,
                timestamp=DetectionResult.utc_timestamp(),
                prediction=prediction,
                label=LABEL_MAPPING[prediction],
                score=score,
                model=self.model_name,
                feature_schema=FEATURE_SCHEMA_VERSION,
                status="CLASSIFIED",
                input_sequence=self.sequence,
                preprocess_time_seconds=preprocess_time,
                inference_time_seconds=inference_time,
                total_time_seconds=total_time,
            )

            if self.logger is not None:
                self.logger.log(result)

            return result

        except Exception:
            total_time = time.perf_counter() - total_start

            result = DetectionResult(
                event_id=event_id,
                timestamp=DetectionResult.utc_timestamp(),
                prediction=None,
                label=None,
                score=None,
                model=self.model_name,
                feature_schema=FEATURE_SCHEMA_VERSION,
                status="ERROR",
                input_sequence=self.sequence,
                total_time_seconds=total_time,
            )

            if self.logger is not None:
                self.logger.log(result)

            return result