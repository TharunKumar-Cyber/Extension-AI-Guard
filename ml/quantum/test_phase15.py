"""
Extension AI Guard - Phase 15 Quantum ML Test Suite.

Validates the Phase 15 quantum configuration, feature map, trained
artifacts, evaluation outputs, and reproducibility metadata.
"""

from __future__ import annotations

import json
from pathlib import Path

import cloudpickle
import joblib
import numpy as np
import pandas as pd

from feature_maps import build_feature_map
from quantum_config import (
    EXPECTED_FEATURE_COUNT,
    EXPECTED_TEST_SAMPLES,
    EXPECTED_TRAIN_SAMPLES,
    FEATURE_MAP_REPS,
    NUM_QUBITS,
    QUANTUM_KERNEL_MATRIX_PATH,
    QUANTUM_KERNEL_MODEL_PATH,
    QUANTUM_KERNEL_NAME,
    QUANTUM_RESULTS_DIR,
    SIMULATOR_BACKEND,
    VQC_ANSATZ_REPS,
    VQC_LOSS_HISTORY_PATH,
    VQC_MODEL_PATH,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

QSVC_EVALUATION_PATH = (
    QUANTUM_RESULTS_DIR / "qsvc_evaluation.csv"
)

VQC_EVALUATION_PATH = (
    QUANTUM_RESULTS_DIR / "vqc_evaluation.csv"
)

UNIFIED_EVALUATION_PATH = (
    QUANTUM_RESULTS_DIR / "quantum_ml_evaluation.csv"
)

METRICS_PATH = (
    QUANTUM_RESULTS_DIR / "quantum_ml_metrics.json"
)

METADATA_PATH = (
    QUANTUM_RESULTS_DIR / "experiment_metadata.json"
)


def test_quantum_configuration() -> None:
    """Verify the core Phase 15 quantum configuration."""

    assert NUM_QUBITS == EXPECTED_FEATURE_COUNT
    assert FEATURE_MAP_REPS == 1
    assert VQC_ANSATZ_REPS == 1
    assert SIMULATOR_BACKEND == "statevector"
    assert QUANTUM_KERNEL_NAME == "fidelity_quantum_kernel"


def test_feature_map() -> None:
    """Verify the quantum feature map dimensions."""

    feature_map = build_feature_map()

    assert feature_map.num_qubits == NUM_QUBITS
    assert feature_map.num_parameters == EXPECTED_FEATURE_COUNT


def test_qsvc_model() -> None:
    """Verify the trained QSVC artifact can be reloaded."""

    assert QUANTUM_KERNEL_MODEL_PATH.exists()

    model = joblib.load(QUANTUM_KERNEL_MODEL_PATH)

    assert type(model).__name__ == "QSVC"
    assert hasattr(model, "predict")
    assert hasattr(model, "decision_function")


def test_vqc_model() -> None:
    """Verify the trained VQC artifact can be reloaded."""

    assert VQC_MODEL_PATH.exists()

    with open(VQC_MODEL_PATH, "rb") as model_file:
        model = cloudpickle.load(model_file)

    assert type(model).__name__ == "VQC"


def test_kernel_matrix() -> None:
    """Verify the generated quantum kernel matrix."""

    assert QUANTUM_KERNEL_MATRIX_PATH.exists()

    kernel_matrix = np.load(
        QUANTUM_KERNEL_MATRIX_PATH
    )

    assert kernel_matrix.shape == (
        EXPECTED_TRAIN_SAMPLES,
        EXPECTED_TRAIN_SAMPLES,
    )

    assert np.isfinite(kernel_matrix).all()

    assert np.allclose(
        kernel_matrix,
        kernel_matrix.T,
        atol=1e-8,
    )

    assert np.allclose(
        np.diag(kernel_matrix),
        1.0,
        atol=1e-6,
    )


def test_vqc_loss_history() -> None:
    """Verify that VQC objective evaluations were recorded."""

    assert VQC_LOSS_HISTORY_PATH.exists()

    loss_history = pd.read_csv(
        VQC_LOSS_HISTORY_PATH
    )

    assert not loss_history.empty
    assert "evaluation" in loss_history.columns
    assert "loss" in loss_history.columns

    assert loss_history["evaluation"].is_monotonic_increasing
    assert np.isfinite(loss_history["loss"]).all()


def test_qsvc_evaluation() -> None:
    """Verify QSVC evaluation output."""

    assert QSVC_EVALUATION_PATH.exists()

    results = pd.read_csv(
        QSVC_EVALUATION_PATH
    )

    assert len(results) == 1

    required_columns = {
        "accuracy",
        "precision",
        "recall",
        "f1",
        "roc_auc",
        "true_negatives",
        "false_positives",
        "false_negatives",
        "true_positives",
    }

    assert required_columns.issubset(
        results.columns
    )


def test_vqc_evaluation() -> None:
    """Verify VQC evaluation output."""

    assert VQC_EVALUATION_PATH.exists()

    results = pd.read_csv(
        VQC_EVALUATION_PATH
    )

    assert len(results) == 1

    required_columns = {
        "accuracy",
        "precision",
        "recall",
        "f1",
        "roc_auc",
        "true_negatives",
        "false_positives",
        "false_negatives",
        "true_positives",
    }

    assert required_columns.issubset(
        results.columns
    )


def test_unified_evaluation() -> None:
    """Verify the consolidated quantum evaluation."""

    assert UNIFIED_EVALUATION_PATH.exists()

    results = pd.read_csv(
        UNIFIED_EVALUATION_PATH
    )

    assert len(results) == 2
    assert set(results["model"]) == {
        "QSVC",
        "VQC",
    }

    assert len(results.columns) >= 10


def test_metrics_json() -> None:
    """Verify the machine-readable metrics artifact."""

    assert METRICS_PATH.exists()

    with open(
        METRICS_PATH,
        "r",
        encoding="utf-8",
    ) as metrics_file:
        metrics = json.load(metrics_file)

    assert "QSVC" in metrics
    assert "VQC" in metrics

    for model_name in ("QSVC", "VQC"):
        assert "accuracy" in metrics[model_name]
        assert "precision" in metrics[model_name]
        assert "recall" in metrics[model_name]
        assert "f1" in metrics[model_name]
        assert "roc_auc" in metrics[model_name]


def test_experiment_metadata() -> None:
    """Verify reproducibility metadata."""

    assert METADATA_PATH.exists()

    with open(
        METADATA_PATH,
        "r",
        encoding="utf-8",
    ) as metadata_file:
        metadata = json.load(metadata_file)

    assert metadata["phase"] == 15
    assert metadata["phase_name"] == (
        "Quantum Machine Learning"
    )
    assert metadata["execution_mode"] == (
        "simulator-first"
    )
    assert metadata["random_state"] == 42

    assert metadata["quantum_kernel"]["qubits"] == (
        NUM_QUBITS
    )

    assert metadata["vqc"]["qubits"] == (
        NUM_QUBITS
    )


def run_tests() -> None:
    """Run all Phase 15 tests."""

    tests = [
        test_quantum_configuration,
        test_feature_map,
        test_qsvc_model,
        test_vqc_model,
        test_kernel_matrix,
        test_vqc_loss_history,
        test_qsvc_evaluation,
        test_vqc_evaluation,
        test_unified_evaluation,
        test_metrics_json,
        test_experiment_metadata,
    ]

    print("Phase 15 test suite started.")

    passed = 0

    for test in tests:
        test()
        passed += 1
        print(f"PASS: {test.__name__}")

    print(
        f"\nPhase 15 test suite completed successfully: "
        f"{passed}/{len(tests)} tests passed."
    )


if __name__ == "__main__":
    run_tests()