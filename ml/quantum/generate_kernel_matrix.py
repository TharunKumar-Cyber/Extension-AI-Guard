"""
Extension AI Guard - Phase 15 Quantum Kernel Matrix Generation.

Generates the training quantum-kernel matrix used by the Phase 15
QSVC experiment and validates its numerical integrity.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from quantum_config import (
    QUANTUM_KERNEL_MATRIX_PATH,
    X_TRAIN_PATH,
    ensure_output_directories,
    validate_configuration,
)
from quantum_kernel import (
    build_quantum_kernel,
    validate_kernel_matrix,
)


def load_training_features() -> np.ndarray:
    """Load the frozen Phase 13 training feature matrix."""

    X_train = pd.read_csv(X_TRAIN_PATH).to_numpy(dtype=float)

    if X_train.shape != (115, 8):
        raise ValueError(
            "Unexpected training feature shape. "
            f"Expected (115, 8), received {X_train.shape}."
        )

    if not np.isfinite(X_train).all():
        raise ValueError("Training features contain non-finite values.")

    return X_train


def generate_kernel_matrix(X_train: np.ndarray) -> np.ndarray:
    """Compute the fidelity quantum-kernel matrix."""

    quantum_kernel = build_quantum_kernel()

    kernel_matrix = quantum_kernel.evaluate(X_train)

    validate_kernel_matrix(kernel_matrix)

    return np.asarray(kernel_matrix, dtype=float)


def save_kernel_matrix(kernel_matrix: np.ndarray) -> None:
    """Save the validated quantum-kernel matrix."""

    ensure_output_directories()
    np.save(QUANTUM_KERNEL_MATRIX_PATH, kernel_matrix)


def main() -> None:
    """Run quantum-kernel matrix generation and validation."""

    validate_configuration()
    ensure_output_directories()

    X_train = load_training_features()

    print("Phase 15 quantum-kernel matrix generation started.")
    print(f"Training samples: {X_train.shape[0]}")
    print(f"Features: {X_train.shape[1]}")

    kernel_matrix = generate_kernel_matrix(X_train)

    save_kernel_matrix(kernel_matrix)

    print("Quantum-kernel matrix generated successfully.")
    print(f"Matrix shape: {kernel_matrix.shape}")
    print(f"Minimum value: {kernel_matrix.min():.12f}")
    print(f"Maximum value: {kernel_matrix.max():.12f}")
    print(f"Mean value: {kernel_matrix.mean():.12f}")
    print(f"Diagonal mean: {np.diag(kernel_matrix).mean():.12f}")
    print(f"Saved: {QUANTUM_KERNEL_MATRIX_PATH}")


if __name__ == "__main__":
    main()