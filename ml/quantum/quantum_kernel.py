"""
Extension AI Guard - Phase 15 Quantum Kernel.

This module constructs and validates the fidelity-based quantum kernel
used by the primary Quantum Support Vector Classifier (QSVC) experiment.

No model training or evaluation logic belongs in this module.
"""

from __future__ import annotations

import numpy as np
from qiskit_machine_learning.kernels import FidelityQuantumKernel

from feature_maps import build_feature_map
from quantum_config import (
    FINITE_VALUE_CHECK_ENABLED,
    KERNEL_SYMMETRY_TOLERANCE,
    NUM_QUBITS,
)


def build_quantum_kernel() -> FidelityQuantumKernel:
    """
    Build the Phase 15 fidelity quantum kernel.

    Returns:
        Configured FidelityQuantumKernel using the Phase 15 feature map.
    """

    feature_map = build_feature_map()

    return FidelityQuantumKernel(
        feature_map=feature_map,
    )


def validate_quantum_kernel() -> FidelityQuantumKernel:
    """
    Validate the Phase 15 quantum-kernel configuration.

    Returns:
        Validated FidelityQuantumKernel instance.

    Raises:
        ValueError: If the feature map does not match the configured
            qubit count or the kernel cannot be constructed.
    """

    kernel = build_quantum_kernel()

    feature_map = kernel.feature_map

    if feature_map.num_qubits != NUM_QUBITS:
        raise ValueError(
            "Quantum-kernel feature-map qubit count does not match "
            f"NUM_QUBITS={NUM_QUBITS}."
        )

    if feature_map.num_parameters != NUM_QUBITS:
        raise ValueError(
            "Quantum-kernel feature-map parameter count does not match "
            f"NUM_QUBITS={NUM_QUBITS}."
        )

    return kernel


def validate_kernel_matrix(
    kernel_matrix: np.ndarray,
    tolerance: float = KERNEL_SYMMETRY_TOLERANCE,
) -> None:
    """
    Validate a computed quantum-kernel matrix.

    The matrix must be square, finite, and symmetric within the configured
    numerical tolerance.

    Args:
        kernel_matrix: Quantum-kernel matrix to validate.
        tolerance: Allowed absolute symmetry difference.

    Raises:
        ValueError: If the matrix violates the validation contract.
    """

    matrix = np.asarray(kernel_matrix, dtype=float)

    if matrix.ndim != 2:
        raise ValueError("Quantum-kernel matrix must be two-dimensional.")

    if matrix.shape[0] != matrix.shape[1]:
        raise ValueError("Quantum-kernel matrix must be square.")

    if FINITE_VALUE_CHECK_ENABLED and not np.isfinite(matrix).all():
        raise ValueError("Quantum-kernel matrix contains non-finite values.")

    if not np.allclose(
        matrix,
        matrix.T,
        atol=tolerance,
        rtol=0.0,
    ):
        raise ValueError(
            "Quantum-kernel matrix is not symmetric within the configured "
            f"tolerance of {tolerance}."
        )


if __name__ == "__main__":
    quantum_kernel = validate_quantum_kernel()

    print("Phase 15 quantum kernel validated successfully.")
    print(f"Kernel: {type(quantum_kernel).__name__}")
    print(f"Feature-map qubits: {quantum_kernel.feature_map.num_qubits}")
    print(
        f"Feature-map parameters: "
        f"{quantum_kernel.feature_map.num_parameters}"
    )
    print(
        f"Kernel symmetry tolerance: "
        f"{KERNEL_SYMMETRY_TOLERANCE}"
    )