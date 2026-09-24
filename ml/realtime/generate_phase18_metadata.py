from __future__ import annotations

import json
import platform
from datetime import datetime, timezone
from pathlib import Path

import joblib
import qiskit
import qiskit_machine_learning
import sklearn

from ml.realtime.realtime_config import (
    DEFAULT_MODEL_NAME,
    FEATURE_SCHEMA_VERSION,
    MODEL_PATHS,
    PREPROCESSOR_PATH,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RESULTS_DIR = PROJECT_ROOT / "ml" / "realtime" / "results"

METADATA_PATH = RESULTS_DIR / "phase18_experiment_metadata.json"
BENCHMARK_PATH = RESULTS_DIR / "phase18_benchmark.json"


def load_benchmark() -> dict[str, float | int]:
    """Load the verified Phase 18 benchmark artifact."""
    with BENCHMARK_PATH.open(
        "r",
        encoding="utf-8",
    ) as handle:
        return json.load(handle)


def generate_metadata() -> dict[str, object]:
    """Generate reproducibility metadata for Phase 18."""
    benchmark = load_benchmark()

    preprocessor = joblib.load(PREPROCESSOR_PATH)

    metadata: dict[str, object] = {
        "phase": 18,
        "phase_name": "Real-Time Detection Engine",
        "experiment_id": "EAG-PHASE18-REALTIME-001",
        "generated_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "project": "Extension AI Guard",
        "feature_schema_version": FEATURE_SCHEMA_VERSION,
        "dataset_contract": {
            "source_phase": 13,
            "training_samples": 115,
            "testing_samples": 29,
            "processed_features": 8,
            "random_state": 42,
            "label_mapping": {
                "0": "BENIGN",
                "1": "MALICIOUS",
            },
        },
        "model_configuration": {
            "default_model": DEFAULT_MODEL_NAME,
            "available_classical_models": sorted(
                MODEL_PATHS.keys()
            ),
            "production_model_status": (
                "configurable engineering model; "
                "not declared as final production model"
            ),
        },
        "preprocessing": {
            "preprocessor_path": str(
                PREPROCESSOR_PATH.relative_to(
                    PROJECT_ROOT
                )
            ),
            "preprocessor_type": type(
                preprocessor
            ).__name__,
        },
        "runtime": {
            "python_version": platform.python_version(),
            "platform": platform.platform(),
            "scikit_learn_version": sklearn.__version__,
            "joblib_version": joblib.__version__,
            "qiskit_version": qiskit.__version__,
            "qiskit_machine_learning_version": (
                qiskit_machine_learning.__version__
            ),
        },
        "realtime_benchmark": benchmark,
        "benchmark_configuration": {
            "samples": benchmark["samples"],
            "observation_protocol": "TCP",
            "observation_http_method": None,
            "observation_frame_len": 512,
            "observation_time_relative": 1.25,
        },
        "pcap_replay": {
            "benign_capture": (
                "dataset/benign_01.pcapng"
            ),
            "controlled_malicious_capture": (
                "dataset/"
                "safe_01_invalid_malicious_test.pcapng"
            ),
            "replay_adapter": (
                "ml/realtime/pcap_replay.py"
            ),
        },
        "quantum_context": {
            "source_phase": 15,
            "qsvc_implemented": True,
            "vqc_implemented": True,
            "quantum_resource_measurements": (
                "recorded in Phase 15/16 artifacts"
            ),
            "realtime_quantum_execution": False,
            "note": (
                "Phase 18 real-time detection uses "
                "configurable classical models. Quantum "
                "models remain part of the research and "
                "comparison track and are not silently "
                "substituted into the realtime engine."
            ),
        },
        "logging": {
            "format": "JSON Lines",
            "logger_module": (
                "ml/realtime/detection_logger.py"
            ),
            "log_file": (
                "ml/realtime/logs/detections.jsonl"
            ),
        },
        "reproducibility": {
            "random_state": 42,
            "simulator_first": True,
            "test_set_tuning": False,
            "dataset_modified_for_realtime": False,
            "phase13_preprocessing_reused": True,
            "benchmark_artifact": (
                "ml/realtime/results/"
                "phase18_benchmark.json"
            ),
        },
        "security_controls": {
            "raw_ip_features_used": False,
            "raw_uri_features_used": False,
            "frame_number_used": False,
            "raw_capture_ports_used": False,
            "input_schema_validation": True,
            "structured_detection_logging": True,
        },
        "limitations": [
            (
                "Phase 18 uses the frozen Phase 13 "
                "feature contract."
            ),
            (
                "The current dataset is small and "
                "controlled."
            ),
            (
                "PCAP replay classification is not "
                "perfect and must not be interpreted "
                "as production validation."
            ),
            (
                "Benchmark measurements are environment-"
                "dependent."
            ),
            (
                "No quantum advantage or production "
                "superiority claim is made."
            ),
        ],
    }

    return metadata


def save_metadata(
    metadata: dict[str, object],
) -> Path:
    """Save Phase 18 metadata as JSON."""
    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    with METADATA_PATH.open(
        "w",
        encoding="utf-8",
    ) as handle:
        json.dump(
            metadata,
            handle,
            indent=2,
        )

    return METADATA_PATH


if __name__ == "__main__":
    metadata = generate_metadata()
    output_path = save_metadata(metadata)

    print(
        json.dumps(
            metadata,
            indent=2,
        )
    )
    print(
        f"result_file={output_path}"
    )