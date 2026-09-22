"""
Extension AI Guard - Phase 15 QSVC Training.

This module trains the primary Phase 15 quantum classifier:
Quantum Support Vector Classifier (QSVC).

The model uses:
- Phase 13 processed training data
- Phase 15 FidelityQuantumKernel
- Fixed random seed and configuration
- Simulator-first execution

No test-set evaluation is performed here.
"""

from __future__ import annotations

import time
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from qiskit_machine_learning.algorithms import QSVC

from quantum_config import (
    QUANTUM_KERNEL_MODEL_PATH,
    X_TRAIN_PATH,
    Y_TRAIN_PATH,
    ensure_output_directories,
    validate_configuration,
)
from quantum_kernel import build_quantum_kernel


def load_training_data() -> tuple[np.ndarray, np.ndarray]:
    """Load the frozen Phase 13 training artifacts."""

    X_train = pd.read_csv(X_TRAIN_PATH).to_numpy(dtype=float)
    y_train = pd.read_csv(Y_TRAIN_PATH).iloc[:, 0].to_numpy(dtype=int)

    if X_train.shape[0] != y_train.shape[0]:
        raise ValueError(
            "Training feature and label sample counts do not match."
        )

    if X_train.shape[1] != 8:
        raise ValueError(
            f"Expected 8 processed features, received {X_train.shape[1]}."
        )

    if not np.isfinite(X_train).all():
        raise ValueError("Training features contain non-finite values.")

    if not np.isin(y_train, [0, 1]).all():
        raise ValueError("Training labels must contain only 0 and 1.")

    return X_train, y_train


def train_qsvc(
    X_train: np.ndarray,
    y_train: np.ndarray,
) -> tuple[QSVC, float]:
    """
    Train the Phase 15 QSVC model.

    Returns:
        Trained QSVC model and training duration in seconds.
    """

    quantum_kernel = build_quantum_kernel()

    model = QSVC(
        quantum_kernel=quantum_kernel,
    )

    start_time = time.perf_counter()
    model.fit(X_train, y_train)
    training_time = time.perf_counter() - start_time

    return model, training_time


def save_qsvc_model(model: QSVC) -> Path:
    """Persist the trained QSVC model."""

    ensure_output_directories()

    joblib.dump(model, QUANTUM_KERNEL_MODEL_PATH)

    return QUANTUM_KERNEL_MODEL_PATH


def main() -> None:
    """Run the complete Phase 15 QSVC training workflow."""

    validate_configuration()
    ensure_output_directories()

    X_train, y_train = load_training_data()

    print("Phase 15 QSVC training started.")
    print(f"Training samples: {X_train.shape[0]}")
    print(f"Features: {X_train.shape[1]}")
    print(
        "Training labels: "
        f"BENIGN={int((y_train == 0).sum())}, "
        f"MALICIOUS={int((y_train == 1).sum())}"
    )

    model, training_time = train_qsvc(X_train, y_train)

    model_path = save_qsvc_model(model)

    print("Phase 15 QSVC training completed successfully.")
    print(f"Training time: {training_time:.6f} seconds")
    print(f"Model saved: {model_path}")


if __name__ == "__main__":
    main()