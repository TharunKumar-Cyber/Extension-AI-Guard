from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from ml.realtime.benchmark_realtime import run_benchmark
from ml.realtime.detection_engine import DetectionEngine
from ml.realtime.detection_logger import DetectionLogger
from ml.realtime.detection_result import DetectionResult
from ml.realtime.feature_adapter import (
    REQUIRED_FIELDS,
    adapt_observation,
    validate_observation,
)
from ml.realtime.pcap_replay import (
    iter_pcap_observations,
    packet_to_observation,
)
from ml.realtime.realtime_config import (
    DEFAULT_MODEL_NAME,
    FEATURE_SCHEMA_VERSION,
    LABEL_MAPPING,
    MODEL_PATHS,
    PREPROCESSOR_PATH,
)
from ml.realtime.replay import detect_batch


PROJECT_ROOT = Path(__file__).resolve().parents[2]

BENIGN_PCAP = PROJECT_ROOT / "dataset" / "benign_01.pcapng"
MALICIOUS_PCAP = (
    PROJECT_ROOT
    / "dataset"
    / "safe_01_invalid_malicious_test.pcapng"
)


VALID_OBSERVATION = {
    "time_relative": 1.25,
    "frame_len": 512,
    "protocol": "TCP",
    "http_method": None,
}


class TestRealtimeConfig(unittest.TestCase):
    def test_preprocessor_exists(self):
        self.assertTrue(PREPROCESSOR_PATH.is_file())

    def test_model_paths_exist(self):
        for model_name, model_path in MODEL_PATHS.items():
            with self.subTest(model=model_name):
                self.assertTrue(model_path.is_file())

    def test_default_model_is_supported(self):
        self.assertIn(DEFAULT_MODEL_NAME, MODEL_PATHS)

    def test_feature_schema_version(self):
        self.assertEqual(FEATURE_SCHEMA_VERSION, "phase13-v1")


class TestFeatureAdapter(unittest.TestCase):
    def test_required_fields(self):
        self.assertEqual(
            REQUIRED_FIELDS,
            (
                "time_relative",
                "frame_len",
                "protocol",
                "http_method",
            ),
        )

    def test_valid_tcp_observation(self):
        observation = adapt_observation(VALID_OBSERVATION)

        self.assertEqual(observation["protocol"], "TCP")
        self.assertIsNone(observation["http_method"])

    def test_valid_http_get_observation(self):
        observation = {
            "time_relative": 2.5,
            "frame_len": 600,
            "protocol": "HTTP",
            "http_method": "GET",
        }

        adapted = adapt_observation(observation)

        self.assertEqual(adapted["protocol"], "HTTP")
        self.assertEqual(adapted["http_method"], "GET")

    def test_valid_http_post_observation(self):
        observation = {
            "time_relative": 3.5,
            "frame_len": 700,
            "protocol": "HTTP/JSON",
            "http_method": "POST",
        }

        adapted = adapt_observation(observation)

        self.assertEqual(adapted["protocol"], "HTTP/JSON")
        self.assertEqual(adapted["http_method"], "POST")

    def test_missing_required_field(self):
        observation = VALID_OBSERVATION.copy()
        del observation["frame_len"]

        with self.assertRaises(ValueError):
            validate_observation(observation)

    def test_invalid_protocol(self):
        observation = VALID_OBSERVATION.copy()
        observation["protocol"] = "FTP"

        with self.assertRaises(ValueError):
            validate_observation(observation)


class TestDetectionResult(unittest.TestCase):
    def test_to_dict(self):
        result = DetectionResult(
            event_id="test-event",
            timestamp="2026-01-01T00:00:00+00:00",
            prediction=1,
            label="MALICIOUS",
            score=0.95,
            model="gradient_boosting",
            feature_schema="phase13-v1",
            status="CLASSIFIED",
        )

        data = result.to_dict()

        self.assertEqual(data["event_id"], "test-event")
        self.assertEqual(data["prediction"], 1)
        self.assertEqual(data["label"], "MALICIOUS")
        self.assertEqual(data["status"], "CLASSIFIED")

    def test_utc_timestamp(self):
        timestamp = DetectionResult.utc_timestamp()

        self.assertIsInstance(timestamp, str)
        self.assertIn("T", timestamp)


class TestDetectionEngine(unittest.TestCase):
    def test_default_engine_initializes(self):
        engine = DetectionEngine()

        self.assertEqual(
            engine.model_name,
            DEFAULT_MODEL_NAME,
        )

    def test_each_classical_model_initializes(self):
        for model_name in MODEL_PATHS:
            with self.subTest(model=model_name):
                engine = DetectionEngine(model_name=model_name)

                self.assertEqual(
                    engine.model_name,
                    model_name,
                )

    def test_unsupported_model(self):
        with self.assertRaises(ValueError):
            DetectionEngine(model_name="unsupported_model")

    def test_tcp_detection(self):
        engine = DetectionEngine()

        result = engine.detect(VALID_OBSERVATION)

        self.assertEqual(result.status, "CLASSIFIED")
        self.assertIn(result.prediction, LABEL_MAPPING)
        self.assertIn(result.label, LABEL_MAPPING.values())

    def test_detection_contains_model_name(self):
        engine = DetectionEngine(
            model_name="gradient_boosting",
        )

        result = engine.detect(VALID_OBSERVATION)

        self.assertEqual(
            result.model,
            "gradient_boosting",
        )

    def test_detection_contains_feature_schema(self):
        engine = DetectionEngine()

        result = engine.detect(VALID_OBSERVATION)

        self.assertEqual(
            result.feature_schema,
            FEATURE_SCHEMA_VERSION,
        )

    def test_detection_contains_sequence(self):
        engine = DetectionEngine()

        first = engine.detect(VALID_OBSERVATION)
        second = engine.detect(VALID_OBSERVATION)

        self.assertEqual(first.input_sequence, 1)
        self.assertEqual(second.input_sequence, 2)

    def test_detection_timing_fields(self):
        engine = DetectionEngine()

        result = engine.detect(VALID_OBSERVATION)

        self.assertIsNotNone(
            result.preprocess_time_seconds,
        )
        self.assertIsNotNone(
            result.inference_time_seconds,
        )
        self.assertIsNotNone(
            result.total_time_seconds,
        )

        self.assertGreaterEqual(
            result.preprocess_time_seconds,
            0,
        )
        self.assertGreaterEqual(
            result.inference_time_seconds,
            0,
        )
        self.assertGreater(
            result.total_time_seconds,
            0,
        )

    def test_invalid_observation_returns_error_result(self):
        engine = DetectionEngine()

        invalid_observation = {
            "time_relative": 1.25,
            "frame_len": 512,
            "protocol": "INVALID",
            "http_method": None,
        }

        result = engine.detect(invalid_observation)

        self.assertEqual(result.status, "ERROR")
        self.assertIsNone(result.prediction)
        self.assertIsNone(result.label)
        self.assertIsNone(result.score)

    def test_prediction_label_mapping(self):
        engine = DetectionEngine()

        result = engine.detect(VALID_OBSERVATION)

        self.assertEqual(
            result.label,
            LABEL_MAPPING[result.prediction],
        )


class TestBatchReplay(unittest.TestCase):
    def test_empty_batch(self):
        results = detect_batch([])

        self.assertEqual(results, [])

    def test_single_observation_batch(self):
        results = detect_batch([VALID_OBSERVATION])

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].status, "CLASSIFIED")

    def test_multiple_observation_batch(self):
        observations = [
            VALID_OBSERVATION,
            VALID_OBSERVATION,
            VALID_OBSERVATION,
        ]

        results = detect_batch(observations)

        self.assertEqual(len(results), 3)

        for result in results:
            self.assertEqual(
                result.status,
                "CLASSIFIED",
            )

    def test_batch_sequence_numbers(self):
        observations = [
            VALID_OBSERVATION,
            VALID_OBSERVATION,
            VALID_OBSERVATION,
        ]

        results = detect_batch(observations)

        sequences = [
            result.input_sequence
            for result in results
        ]

        self.assertEqual(
            sequences,
            [1, 2, 3],
        )


class TestDetectionLogger(unittest.TestCase):
    def test_logger_creates_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            log_path = Path(temp_dir) / "detections.jsonl"
            logger = DetectionLogger(log_path)

            result = DetectionResult(
                event_id="test-event",
                timestamp="2026-01-01T00:00:00+00:00",
                prediction=1,
                label="MALICIOUS",
                score=0.9,
                model="gradient_boosting",
                feature_schema="phase13-v1",
                status="CLASSIFIED",
            )

            logger.log(result)

            self.assertTrue(log_path.is_file())

    def test_logger_round_trip(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            log_path = Path(temp_dir) / "detections.jsonl"
            logger = DetectionLogger(log_path)

            result = DetectionResult(
                event_id="round-trip-event",
                timestamp="2026-01-01T00:00:00+00:00",
                prediction=1,
                label="MALICIOUS",
                score=0.9,
                model="gradient_boosting",
                feature_schema="phase13-v1",
                status="CLASSIFIED",
            )

            logger.log(result)

            records = logger.read_all()

            self.assertEqual(len(records), 1)
            self.assertEqual(
                records[0]["event_id"],
                "round-trip-event",
            )
            self.assertEqual(
                records[0]["label"],
                "MALICIOUS",
            )


class TestPCAPReplay(unittest.TestCase):
    def test_benign_pcap_exists(self):
        self.assertTrue(BENIGN_PCAP.is_file())

    def test_malicious_pcap_exists(self):
        self.assertTrue(MALICIOUS_PCAP.is_file())

    def test_benign_pcap_produces_observations(self):
        observations = list(
            iter_pcap_observations(BENIGN_PCAP)
        )

        self.assertGreater(len(observations), 0)

        for observation in observations:
            self.assertIn(
                "time_relative",
                observation,
            )
            self.assertIn(
                "frame_len",
                observation,
            )
            self.assertIn(
                "protocol",
                observation,
            )
            self.assertIn(
                "http_method",
                observation,
            )

    def test_malicious_pcap_produces_observations(self):
        observations = list(
            iter_pcap_observations(MALICIOUS_PCAP)
        )

        self.assertGreater(len(observations), 0)

        for observation in observations:
            self.assertIn(
                observation["protocol"],
                {"HTTP", "HTTP/JSON", "TCP"},
            )


class TestPhase18Benchmark(unittest.TestCase):
    def test_benchmark_returns_expected_fields(self):
        result = run_benchmark(samples=5)

        expected_fields = {
            "samples",
            "wall_time_seconds",
            "throughput_per_second",
            "avg_detection_ms",
            "min_detection_ms",
            "max_detection_ms",
            "errors",
        }

        self.assertEqual(
            set(result.keys()),
            expected_fields,
        )

    def test_benchmark_completes_without_errors(self):
        result = run_benchmark(samples=5)

        self.assertEqual(
            result["samples"],
            5,
        )
        self.assertEqual(
            result["errors"],
            0,
        )

    def test_benchmark_metrics_are_positive(self):
        result = run_benchmark(samples=5)

        self.assertGreater(
            result["wall_time_seconds"],
            0,
        )
        self.assertGreater(
            result["throughput_per_second"],
            0,
        )
        self.assertGreater(
            result["avg_detection_ms"],
            0,
        )
        self.assertGreater(
            result["min_detection_ms"],
            0,
        )
        self.assertGreater(
            result["max_detection_ms"],
            0,
        )

    def test_benchmark_latency_order(self):
        result = run_benchmark(samples=5)

        self.assertLessEqual(
            result["min_detection_ms"],
            result["avg_detection_ms"],
        )

        self.assertLessEqual(
            result["avg_detection_ms"],
            result["max_detection_ms"],
        )


if __name__ == "__main__":
    unittest.main()