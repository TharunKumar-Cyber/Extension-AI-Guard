from __future__ import annotations

import json
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RESULTS_DIR = PROJECT_ROOT / "ml" / "realtime" / "results"

BENCHMARK_PATH = RESULTS_DIR / "phase18_benchmark.json"

METADATA_PATH = (
    RESULTS_DIR / "phase18_experiment_metadata.json"
)


class TestPhase18Artifacts(unittest.TestCase):
    def test_results_directory_exists(self):
        self.assertTrue(RESULTS_DIR.is_dir())

    def test_benchmark_artifact_exists(self):
        self.assertTrue(BENCHMARK_PATH.is_file())

    def test_benchmark_artifact_contains_valid_json(self):
        with BENCHMARK_PATH.open(
            "r",
            encoding="utf-8",
        ) as handle:
            data = json.load(handle)

        self.assertIsInstance(data, dict)

    def test_benchmark_artifact_contains_required_fields(self):
        with BENCHMARK_PATH.open(
            "r",
            encoding="utf-8",
        ) as handle:
            data = json.load(handle)

        required_fields = {
            "samples",
            "wall_time_seconds",
            "throughput_per_second",
            "avg_detection_ms",
            "min_detection_ms",
            "max_detection_ms",
            "errors",
        }

        self.assertTrue(
            required_fields.issubset(data.keys())
        )

    def test_benchmark_artifact_values_are_valid(self):
        with BENCHMARK_PATH.open(
            "r",
            encoding="utf-8",
        ) as handle:
            data = json.load(handle)

        self.assertGreater(data["samples"], 0)
        self.assertGreater(
            data["wall_time_seconds"],
            0,
        )
        self.assertGreater(
            data["throughput_per_second"],
            0,
        )
        self.assertGreater(
            data["avg_detection_ms"],
            0,
        )
        self.assertGreaterEqual(
            data["min_detection_ms"],
            0,
        )
        self.assertGreaterEqual(
            data["max_detection_ms"],
            data["min_detection_ms"],
        )
        self.assertEqual(
            data["errors"],
            0,
        )

    def test_metadata_artifact_exists(self):
        self.assertTrue(METADATA_PATH.is_file())

    def test_metadata_artifact_contains_valid_json(self):
        with METADATA_PATH.open(
            "r",
            encoding="utf-8",
        ) as handle:
            data = json.load(handle)

        self.assertIsInstance(data, dict)

    def test_metadata_phase_and_experiment(self):
        with METADATA_PATH.open(
            "r",
            encoding="utf-8",
        ) as handle:
            data = json.load(handle)

        self.assertEqual(data["phase"], 18)
        self.assertEqual(
            data["phase_name"],
            "Real-Time Detection Engine",
        )
        self.assertEqual(
            data["experiment_id"],
            "EAG-PHASE18-REALTIME-001",
        )

    def test_metadata_dataset_contract(self):
        with METADATA_PATH.open(
            "r",
            encoding="utf-8",
        ) as handle:
            data = json.load(handle)

        contract = data["dataset_contract"]

        self.assertEqual(contract["source_phase"], 13)
        self.assertEqual(contract["training_samples"], 115)
        self.assertEqual(contract["testing_samples"], 29)
        self.assertEqual(contract["processed_features"], 8)
        self.assertEqual(contract["random_state"], 42)

    def test_metadata_runtime_and_quantum_context(self):
        with METADATA_PATH.open(
            "r",
            encoding="utf-8",
        ) as handle:
            data = json.load(handle)

        runtime = data["runtime"]
        quantum = data["quantum_context"]

        self.assertEqual(
            runtime["python_version"],
            "3.13.9",
        )
        self.assertEqual(
            runtime["qiskit_version"],
            "2.5.2",
        )
        self.assertEqual(
            runtime["qiskit_machine_learning_version"],
            "0.9.1",
        )

        self.assertTrue(quantum["qsvc_implemented"])
        self.assertTrue(quantum["vqc_implemented"])
        self.assertFalse(
            quantum["realtime_quantum_execution"]
        )

    def test_metadata_security_controls(self):
        with METADATA_PATH.open(
            "r",
            encoding="utf-8",
        ) as handle:
            data = json.load(handle)

        security = data["security_controls"]

        self.assertFalse(
            security["raw_ip_features_used"]
        )
        self.assertFalse(
            security["raw_uri_features_used"]
        )
        self.assertFalse(
            security["frame_number_used"]
        )
        self.assertFalse(
            security["raw_capture_ports_used"]
        )
        self.assertTrue(
            security["input_schema_validation"]
        )
        self.assertTrue(
            security["structured_detection_logging"]
        )


if __name__ == "__main__":
    unittest.main()