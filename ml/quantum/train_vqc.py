"""
Extension AI Guard - Phase 15 VQC Training.

This module trains the secondary Phase 15 quantum classifier:
Variational Quantum Classifier (VQC).

The experiment uses:
- Phase 13 processed training data
- Phase 15 ZZ feature map
- RealAmplitudes ansatz
- COBYLA optimizer
- StatevectorSampler
- Fixed Phase 15 configuration
- Objective-value loss recording

No test-set evaluation is performed here.
"""

from __future__ import annotations

import time
from pathlib import Path

import cloudpickle
import numpy as np
import pandas as pd
from qiskit.circuit.library import real_amplitudes
from qiskit.primitives import StatevectorSampler
from qiskit_algorithms.optimizers import COBYLA
from qiskit_machine_learning.algorithms import VQC

from feature_maps import build_feature_map
from quantum_config import (
    VQC_LOSS_HISTORY_PATH,
    VQC_MODEL_PATH,
    VQC_OPTIMIZER_MAXITER,
    VQC_ANSATZ_REPS,
    VQC_TOLERANCE,
    X_TRAIN_PATH,
    Y_TRAIN_PATH,
    ensure_output_directories,
    validate_configuration,
)


class LossTrackingCOBYLA(COBYLA):
    """COBYLA optimizer wrapper that records actual objective evaluations."""

    def __init__(
        self,
        loss_history: list[float],
        *,
        maxiter: int,
        tol: float,
    ) -> None:
        self.loss_history = loss_history

        super().__init__(
            maxiter=maxiter,
            tol=tol,
        )

    def minimize(
        self,
        fun,
        x0,
        jac=None,
        bounds=None,
    ):
        """Run COBYLA while recording every objective evaluation."""

        def tracked_objective(parameters):
            objective_value = float(fun(parameters))
            self.loss_history.append(objective_value)
            return objective_value

        return super().minimize(
            fun=tracked_objective,
            x0=x0,
            jac=jac,
            bounds=bounds,
        )


def load_training_data() -> tuple[np.ndarray, np.ndarray]:
    """Load the frozen Phase 13 training artifacts."""

    X_train = pd.read_csv(X_TRAIN_PATH).to_numpy(dtype=float)
    y_train = pd.read_csv(Y_TRAIN_PATH).iloc[:, 0].to_numpy(dtype=int)

    if X_train.shape != (115, 8):
        raise ValueError(
            "Unexpected training feature shape. "
            f"Expected (115, 8), received {X_train.shape}."
        )

    if X_train.shape[0] != y_train.shape[0]:
        raise ValueError(
            "Training feature and label sample counts do not match."
        )

    if not np.isfinite(X_train).all():
        raise ValueError("Training features contain non-finite values.")

    if not np.isin(y_train, [0, 1]).all():
        raise ValueError("Training labels must contain only 0 and 1.")

    return X_train, y_train


def build_vqc(
    loss_history: list[float],
) -> VQC:
    """
    Build the configured Phase 15 VQC.

    Args:
        loss_history: Mutable list used to record objective values.

    Returns:
        Configured VQC instance.
    """

    feature_map = build_feature_map()

    ansatz = real_amplitudes(
        num_qubits=feature_map.num_qubits,
        reps=VQC_ANSATZ_REPS,
        entanglement="linear",
    )

    optimizer = LossTrackingCOBYLA(
        loss_history=loss_history,
        maxiter=VQC_OPTIMIZER_MAXITER,
        tol=VQC_TOLERANCE,
    )

    sampler = StatevectorSampler(
        default_shots=1024,
        seed=42,
    )

    return VQC(
        num_qubits=feature_map.num_qubits,
        feature_map=feature_map,
        ansatz=ansatz,
        loss="cross_entropy",
        optimizer=optimizer,
        sampler=sampler,
    )


def save_loss_history(loss_history: list[float]) -> Path:
    """Save VQC objective-value history as CSV."""

    ensure_output_directories()

    loss_frame = pd.DataFrame(
        {
            "evaluation": np.arange(1, len(loss_history) + 1),
            "loss": loss_history,
        }
    )

    loss_frame.to_csv(VQC_LOSS_HISTORY_PATH, index=False)

    return VQC_LOSS_HISTORY_PATH


def save_vqc_model(model: VQC) -> Path:
    """Persist the trained VQC model using cloudpickle."""

    ensure_output_directories()

    with open(VQC_MODEL_PATH, "wb") as model_file:
        cloudpickle.dump(model, model_file)

    return VQC_MODEL_PATH


def main() -> None:
    """Run the complete Phase 15 VQC training workflow."""

    validate_configuration()
    ensure_output_directories()

    X_train, y_train = load_training_data()

    print("Phase 15 VQC training started.")
    print(f"Training samples: {X_train.shape[0]}")
    print(f"Features: {X_train.shape[1]}")
    print(
        "Training labels: "
        f"BENIGN={int((y_train == 0).sum())}, "
        f"MALICIOUS={int((y_train == 1).sum())}"
    )
    print(f"VQC ansatz repetitions: {VQC_ANSATZ_REPS}")
    print(f"COBYLA maximum iterations: {VQC_OPTIMIZER_MAXITER}")
    print(f"COBYLA tolerance: {VQC_TOLERANCE}")

    loss_history: list[float] = []

    model = build_vqc(loss_history)

    start_time = time.perf_counter()
    model.fit(X_train, y_train)
    training_time = time.perf_counter() - start_time

    model_path = save_vqc_model(model)
    loss_path = save_loss_history(loss_history)

    print("Phase 15 VQC training completed successfully.")
    print(f"Training time: {training_time:.6f} seconds")
    print(f"Objective evaluations recorded: {len(loss_history)}")
    print(f"Model saved: {model_path}")
    print(f"Loss history saved: {loss_path}")

    if loss_history:
        print(f"Initial loss: {loss_history[0]:.12f}")
        print(f"Final loss: {loss_history[-1]:.12f}")
        print(f"Minimum loss: {min(loss_history):.12f}")


if __name__ == "__main__":
    main()