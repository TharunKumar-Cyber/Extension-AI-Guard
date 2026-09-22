from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from quantum_config import (
    CLASSICAL_CONTROL,
    CONFIG_VERSION,
    ENTANGLEMENT,
    EXECUTION_MODE,
    FEATURE_MAP_REPS,
    NUM_QUBITS,
    PHASE,
    PHASE_NAME,
    QUANTUM_KERNEL_MATRIX_PATH,
    QUANTUM_KERNEL_NAME,
    QUANTUM_KERNEL_MODEL_PATH,
    QUANTUM_RESULTS_DIR,
    RANDOM_STATE,
    SIMULATOR_BACKEND,
    VQC_ANSATZ_REPS,
    VQC_LOSS_HISTORY_PATH,
    VQC_MODEL_PATH,
    VQC_OPTIMIZER_MAXITER,
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


def require_file(path: Path, description: str) -> None:
    """Verify that a required Phase 15 artifact exists."""

    if not path.exists():
        raise FileNotFoundError(
            f"Required {description} not found: {path}"
        )


def load_evaluation_results(
    path: Path,
    model_name: str,
) -> pd.DataFrame:
    """Load and validate one model's evaluation result."""

    require_file(path, f"{model_name} evaluation")

    frame = pd.read_csv(path)

    if frame.empty:
        raise ValueError(
            f"{model_name} evaluation file is empty: {path}"
        )

    frame.insert(0, "model", model_name)

    return frame


def build_unified_evaluation() -> pd.DataFrame:
    """Combine QSVC and VQC test-set evaluation results."""

    qsvc = load_evaluation_results(
        QSVC_EVALUATION_PATH,
        "QSVC",
    )

    vqc = load_evaluation_results(
        VQC_EVALUATION_PATH,
        "VQC",
    )

    unified = pd.concat(
        [qsvc, vqc],
        ignore_index=True,
    )

    required_columns = {
        "model",
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

    missing_columns = required_columns.difference(
        unified.columns
    )

    if missing_columns:
        raise ValueError(
            "Unified evaluation is missing columns: "
            f"{sorted(missing_columns)}"
        )

    return unified


def build_metrics(unified: pd.DataFrame) -> dict:
    """Create a machine-readable Phase 15 metrics summary."""

    metrics: dict = {}

    for _, row in unified.iterrows():
        model_name = str(row["model"])

        metrics[model_name] = {
            "accuracy": float(row["accuracy"]),
            "precision": float(row["precision"]),
            "recall": float(row["recall"]),
            "f1": float(row["f1"]),
            "roc_auc": float(row["roc_auc"]),
            "true_negatives": int(row["true_negatives"]),
            "false_positives": int(row["false_positives"]),
            "false_negatives": int(row["false_negatives"]),
            "true_positives": int(row["true_positives"]),
        }

    return metrics


def build_metadata() -> dict:
    """Create reproducibility metadata for Phase 15."""

    require_file(
        QUANTUM_KERNEL_MODEL_PATH,
        "QSVC model",
    )

    require_file(
        QUANTUM_KERNEL_MATRIX_PATH,
        "quantum kernel matrix",
    )

    require_file(
        VQC_MODEL_PATH,
        "VQC model",
    )

    require_file(
        VQC_LOSS_HISTORY_PATH,
        "VQC loss history",
    )

    kernel_matrix = pd.read_csv(
        QUANTUM_KERNEL_MATRIX_PATH,
        header=None,
    ) if QUANTUM_KERNEL_MATRIX_PATH.suffix == ".csv" else None

    metadata = {
        "phase": PHASE,
        "phase_name": PHASE_NAME,
        "config_version": CONFIG_VERSION,
        "execution_mode": EXECUTION_MODE,
        "random_state": RANDOM_STATE,
        "classical_control": CLASSICAL_CONTROL,
        "quantum_kernel": {
            "name": QUANTUM_KERNEL_NAME,
            "qubits": NUM_QUBITS,
            "feature_map_repetitions": FEATURE_MAP_REPS,
            "entanglement": ENTANGLEMENT,
            "simulator_backend": SIMULATOR_BACKEND,
            "model_path": str(
                QUANTUM_KERNEL_MODEL_PATH.relative_to(
                    PROJECT_ROOT
                )
            ),
            "kernel_matrix_path": str(
                QUANTUM_KERNEL_MATRIX_PATH.relative_to(
                    PROJECT_ROOT
                )
            ),
        },
        "vqc": {
            "qubits": NUM_QUBITS,
            "ansatz_repetitions": VQC_ANSATZ_REPS,
            "ansatz_entanglement": ENTANGLEMENT,
            "optimizer": "COBYLA",
            "optimizer_max_iterations": VQC_OPTIMIZER_MAXITER,
            "model_path": str(
                VQC_MODEL_PATH.relative_to(PROJECT_ROOT)
            ),
            "loss_history_path": str(
                VQC_LOSS_HISTORY_PATH.relative_to(
                    PROJECT_ROOT
                )
            ),
        },
        "generated_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),
    }

    return metadata


def main() -> None:
    """Build unified Phase 15 quantum artifacts."""

    print("Phase 15 unified quantum-results build started.")

    QUANTUM_RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    unified = build_unified_evaluation()

    unified.to_csv(
        UNIFIED_EVALUATION_PATH,
        index=False,
    )

    metrics = build_metrics(unified)

    with open(
        METRICS_PATH,
        "w",
        encoding="utf-8",
    ) as metrics_file:
        json.dump(
            metrics,
            metrics_file,
            indent=2,
        )

    metadata = build_metadata()

    with open(
        METADATA_PATH,
        "w",
        encoding="utf-8",
    ) as metadata_file:
        json.dump(
            metadata,
            metadata_file,
            indent=2,
        )

    print(
        "Unified quantum evaluation saved:",
        UNIFIED_EVALUATION_PATH,
    )

    print(
        "Quantum metrics saved:",
        METRICS_PATH,
    )

    print(
        "Experiment metadata saved:",
        METADATA_PATH,
    )

    print("\nPhase 15 quantum evaluation summary:")

    for _, row in unified.iterrows():
        print(
            f"{row['model']}: "
            f"Accuracy={row['accuracy']:.4f}, "
            f"Precision={row['precision']:.4f}, "
            f"Recall={row['recall']:.4f}, "
            f"F1={row['f1']:.4f}, "
            f"ROC-AUC={row['roc_auc']:.4f}"
        )

    print(
        "\nPhase 15 unified quantum-results build "
        "completed successfully."
    )


if __name__ == "__main__":
    main()