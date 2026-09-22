"""
Extension AI Guard - Phase 15 Quantum ML Configuration.

This module contains the single source of configuration for the Phase 15
quantum machine learning experiments.

The configuration is intentionally centralized so that quantum experiments
remain reproducible and use the same Phase 13 preprocessing contract.
"""

from __future__ import annotations

from pathlib import Path


# ---------------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PREPROCESSING_DIR = PROJECT_ROOT / "ml" / "preprocessing"
PREPROCESSING_ARTIFACTS_DIR = PREPROCESSING_DIR / "artifacts"

QUANTUM_DIR = PROJECT_ROOT / "ml" / "quantum"
QUANTUM_ARTIFACTS_DIR = QUANTUM_DIR / "artifacts"
QUANTUM_RESULTS_DIR = QUANTUM_DIR / "results"

QUANTUM_KERNEL_ARTIFACTS_DIR = QUANTUM_ARTIFACTS_DIR / "quantum_kernel"
VQC_ARTIFACTS_DIR = QUANTUM_ARTIFACTS_DIR / "vqc"


# ---------------------------------------------------------------------------
# Phase 13 input artifacts
# ---------------------------------------------------------------------------

X_TRAIN_PATH = PREPROCESSING_ARTIFACTS_DIR / "X_train.csv"
X_TEST_PATH = PREPROCESSING_ARTIFACTS_DIR / "X_test.csv"
Y_TRAIN_PATH = PREPROCESSING_ARTIFACTS_DIR / "y_train.csv"
Y_TEST_PATH = PREPROCESSING_ARTIFACTS_DIR / "y_test.csv"

PREPROCESSOR_PATH = PREPROCESSING_ARTIFACTS_DIR / "preprocessor.joblib"
FEATURE_METADATA_PATH = PREPROCESSING_ARTIFACTS_DIR / "feature_metadata.csv"
LABEL_MAPPING_PATH = PREPROCESSING_ARTIFACTS_DIR / "label_mapping.csv"


# ---------------------------------------------------------------------------
# Dataset contract
# ---------------------------------------------------------------------------

RANDOM_STATE = 42

EXPECTED_FEATURE_COUNT = 8

EXPECTED_TRAIN_SAMPLES = 115
EXPECTED_TEST_SAMPLES = 29

EXPECTED_TRAIN_BENIGN = 89
EXPECTED_TRAIN_MALICIOUS = 26

EXPECTED_TEST_BENIGN = 23
EXPECTED_TEST_MALICIOUS = 6


# ---------------------------------------------------------------------------
# Quantum circuit configuration
# ---------------------------------------------------------------------------

NUM_QUBITS = EXPECTED_FEATURE_COUNT

FEATURE_MAP_REPS = 1

ENTANGLEMENT = "linear"

CIRCUIT_SIMPLIFICATION = True


# ---------------------------------------------------------------------------
# Quantum kernel configuration
# ---------------------------------------------------------------------------

QUANTUM_KERNEL_NAME = "fidelity_quantum_kernel"

QSVC_ENABLED = True


# ---------------------------------------------------------------------------
# VQC configuration
# ---------------------------------------------------------------------------

VQC_ENABLED = True

VQC_ANSATZ_REPS = 1

VQC_OPTIMIZER_MAXITER = 100

VQC_TOLERANCE = 1e-3


# ---------------------------------------------------------------------------
# Simulator configuration
# ---------------------------------------------------------------------------

SIMULATOR_BACKEND = "statevector"

SIMULATOR_SHOTS = None


# ---------------------------------------------------------------------------
# Numerical validation configuration
# ---------------------------------------------------------------------------

KERNEL_SYMMETRY_TOLERANCE = 1e-8

FINITE_VALUE_CHECK_ENABLED = True


# ---------------------------------------------------------------------------
# Output artifacts
# ---------------------------------------------------------------------------

QUANTUM_KERNEL_MODEL_PATH = (
    QUANTUM_KERNEL_ARTIFACTS_DIR / "qsvc_model.joblib"
)

VQC_MODEL_PATH = VQC_ARTIFACTS_DIR / "vqc_model.joblib"

QUANTUM_KERNEL_MATRIX_PATH = (
    QUANTUM_KERNEL_ARTIFACTS_DIR / "kernel_matrix.npy"
)

VQC_LOSS_HISTORY_PATH = VQC_ARTIFACTS_DIR / "loss_history.csv"

QUANTUM_EVALUATION_PATH = (
    QUANTUM_RESULTS_DIR / "quantum_ml_evaluation.csv"
)

QUANTUM_METRICS_PATH = (
    QUANTUM_RESULTS_DIR / "quantum_ml_metrics.json"
)

EXPERIMENT_METADATA_PATH = (
    QUANTUM_RESULTS_DIR / "experiment_metadata.json"
)


# ---------------------------------------------------------------------------
# Reproducibility metadata
# ---------------------------------------------------------------------------

CONFIG_VERSION = "phase15-v1"

PHASE = 15

PHASE_NAME = "Quantum Machine Learning"

CLASSICAL_CONTROL = "RBF SVM"

EXECUTION_MODE = "simulator-first"


def validate_configuration() -> None:
    """
    Validate the static Phase 15 configuration.

    Raises:
        ValueError: If a configuration value violates the Phase 15 contract.
    """

    if EXPECTED_FEATURE_COUNT <= 0:
        raise ValueError("EXPECTED_FEATURE_COUNT must be positive.")

    if NUM_QUBITS != EXPECTED_FEATURE_COUNT:
        raise ValueError(
            "NUM_QUBITS must match EXPECTED_FEATURE_COUNT for the initial "
            "one-feature-to-one-qubit configuration."
        )

    if FEATURE_MAP_REPS <= 0:
        raise ValueError("FEATURE_MAP_REPS must be positive.")

    if VQC_ANSATZ_REPS <= 0:
        raise ValueError("VQC_ANSATZ_REPS must be positive.")

    if VQC_OPTIMIZER_MAXITER <= 0:
        raise ValueError("VQC_OPTIMIZER_MAXITER must be positive.")

    if VQC_TOLERANCE <= 0:
        raise ValueError("VQC_TOLERANCE must be positive.")

    if KERNEL_SYMMETRY_TOLERANCE <= 0:
        raise ValueError("KERNEL_SYMMETRY_TOLERANCE must be positive.")

    if not (0 <= EXPECTED_TRAIN_BENIGN <= EXPECTED_TRAIN_SAMPLES):
        raise ValueError("Invalid expected training BENIGN count.")

    if not (0 <= EXPECTED_TRAIN_MALICIOUS <= EXPECTED_TRAIN_SAMPLES):
        raise ValueError("Invalid expected training MALICIOUS count.")

    if not (0 <= EXPECTED_TEST_BENIGN <= EXPECTED_TEST_SAMPLES):
        raise ValueError("Invalid expected test BENIGN count.")

    if not (0 <= EXPECTED_TEST_MALICIOUS <= EXPECTED_TEST_SAMPLES):
        raise ValueError("Invalid expected test MALICIOUS count.")

    if EXPECTED_TRAIN_BENIGN + EXPECTED_TRAIN_MALICIOUS != EXPECTED_TRAIN_SAMPLES:
        raise ValueError(
            "Expected training class counts do not match training size."
        )

    if EXPECTED_TEST_BENIGN + EXPECTED_TEST_MALICIOUS != EXPECTED_TEST_SAMPLES:
        raise ValueError(
            "Expected test class counts do not match test size."
        )


def ensure_output_directories() -> None:
    """Create Phase 15 artifact and result directories if required."""

    QUANTUM_KERNEL_ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    VQC_ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    QUANTUM_RESULTS_DIR.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    validate_configuration()
    ensure_output_directories()
    print("Phase 15 quantum configuration validated successfully.")
    print(f"Configuration version: {CONFIG_VERSION}")
    print(f"Qubits: {NUM_QUBITS}")
    print(f"Feature-map repetitions: {FEATURE_MAP_REPS}")
    print(f"Entanglement: {ENTANGLEMENT}")
    print(f"VQC ansatz repetitions: {VQC_ANSATZ_REPS}")
    print(f"VQC max iterations: {VQC_OPTIMIZER_MAXITER}")
    print(f"Execution mode: {EXECUTION_MODE}")