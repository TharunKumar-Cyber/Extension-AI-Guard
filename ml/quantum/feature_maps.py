"""
Extension AI Guard - Phase 15 Quantum Feature Maps.

This module defines the quantum feature-map construction used by the
Phase 15 experiments.

The implementation uses the non-deprecated ``zz_feature_map`` function
provided by the installed Qiskit 2.x API.

No model training or evaluation logic belongs in this module.
"""

from __future__ import annotations

from qiskit import QuantumCircuit
from qiskit.circuit.library import zz_feature_map

from quantum_config import (
    ENTANGLEMENT,
    EXPECTED_FEATURE_COUNT,
    FEATURE_MAP_REPS,
    NUM_QUBITS,
)


def build_feature_map(
    num_qubits: int = NUM_QUBITS,
    reps: int = FEATURE_MAP_REPS,
    entanglement: str = ENTANGLEMENT,
) -> QuantumCircuit:
    """
    Build the Phase 15 ZZ feature map.

    Args:
        num_qubits: Number of qubits used by the feature map.
        reps: Number of repetitions of the feature-map structure.
        entanglement: Entanglement strategy used by the feature map.

    Returns:
        Configured ZZ feature-map quantum circuit.

    Raises:
        ValueError: If the requested configuration violates the Phase 15
            one-feature-to-one-qubit design.
    """

    if num_qubits <= 0:
        raise ValueError("num_qubits must be positive.")

    if reps <= 0:
        raise ValueError("reps must be positive.")

    if num_qubits != EXPECTED_FEATURE_COUNT:
        raise ValueError(
            "Phase 15 currently requires one qubit per processed feature. "
            f"Expected {EXPECTED_FEATURE_COUNT} qubits, received {num_qubits}."
        )

    feature_map = zz_feature_map(
        feature_dimension=num_qubits,
        reps=reps,
        entanglement=entanglement,
    )

    return feature_map


def build_feature_map_circuit() -> QuantumCircuit:
    """
    Build the default Phase 15 feature-map circuit.

    Returns:
        Default configured ZZ feature-map circuit.
    """

    return build_feature_map()


def validate_feature_map() -> QuantumCircuit:
    """
    Validate the default feature-map configuration.

    Returns:
        Validated feature-map circuit.

    Raises:
        ValueError: If the circuit does not satisfy the Phase 15 contract.
    """

    circuit = build_feature_map_circuit()

    if circuit.num_qubits != EXPECTED_FEATURE_COUNT:
        raise ValueError(
            "Feature-map qubit count does not match the Phase 15 feature count."
        )

    if circuit.num_parameters != EXPECTED_FEATURE_COUNT:
        raise ValueError(
            "Feature-map parameter count does not match the Phase 15 "
            "feature count."
        )

    if circuit.depth() <= 0:
        raise ValueError("Feature-map circuit depth must be positive.")

    return circuit


if __name__ == "__main__":
    feature_map = validate_feature_map()

    print("Phase 15 feature map validated successfully.")
    print(f"Feature map: {feature_map.name}")
    print(f"Qubits: {feature_map.num_qubits}")
    print(f"Parameters: {feature_map.num_parameters}")
    print(f"Depth: {feature_map.depth()}")
    print(f"Size: {feature_map.size()}")
    print(f"Entanglement: {ENTANGLEMENT}")
    print(f"Repetitions: {FEATURE_MAP_REPS}")