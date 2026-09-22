"""
Extension AI Guard - Phase 15 VQC Evaluation.

This module evaluates the trained Phase 15 VQC model on the untouched
Phase 13 test set.

No training is performed here.
"""

from __future__ import annotations

import time

import cloudpickle
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

from quantum_config import (
    QUANTUM_RESULTS_DIR,
    VQC_MODEL_PATH,
    X_TEST_PATH,
    Y_TEST_PATH,
)


def load_test_data() -> tuple[np.ndarray, np.ndarray]:
    """Load the frozen Phase 13 test artifacts."""

    X_test = pd.read_csv(X_TEST_PATH).to_numpy(dtype=float)
    y_test = pd.read_csv(Y_TEST_PATH).iloc[:, 0].to_numpy(dtype=int)

    if X_test.shape != (29, 8):
        raise ValueError(
            "Unexpected test feature shape. "
            f"Expected (29, 8), received {X_test.shape}."
        )

    if X_test.shape[0] != y_test.shape[0]:
        raise ValueError(
            "Test feature and label sample counts do not match."
        )

    if not np.isfinite(X_test).all():
        raise ValueError("Test features contain non-finite values.")

    if not np.isin(y_test, [0, 1]).all():
        raise ValueError("Test labels must contain only 0 and 1.")

    return X_test, y_test


def load_vqc_model():
    """Load the trained VQC model using cloudpickle."""

    with open(VQC_MODEL_PATH, "rb") as model_file:
        model = cloudpickle.load(model_file)

    return model


def main() -> None:
    """Evaluate the trained VQC model."""

    X_test, y_test = load_test_data()
    model = load_vqc_model()

    print("Phase 15 VQC evaluation started.")
    print(f"Test samples: {X_test.shape[0]}")
    print(f"Features: {X_test.shape[1]}")
    print(
        "Test labels: "
        f"BENIGN={int((y_test == 0).sum())}, "
        f"MALICIOUS={int((y_test == 1).sum())}"
    )

    start_time = time.perf_counter()
    predictions = model.predict(X_test)
    inference_time = time.perf_counter() - start_time

    predictions = np.asarray(predictions).reshape(-1).astype(int)

    if predictions.shape[0] != y_test.shape[0]:
        raise ValueError(
            "Prediction and test-label sample counts do not match."
        )

    if not np.isin(predictions, [0, 1]).all():
        raise ValueError("VQC predictions must contain only 0 and 1.")

    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(
        y_test,
        predictions,
        zero_division=0,
    )
    recall = recall_score(
        y_test,
        predictions,
        zero_division=0,
    )
    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0,
    )

    try:
        probabilities = model.predict_proba(X_test)
        probabilities = np.asarray(probabilities)

        if probabilities.ndim == 2 and probabilities.shape[1] >= 2:
            malicious_probability = probabilities[:, 1]
            roc_auc = roc_auc_score(
                y_test,
                malicious_probability,
            )
        else:
            roc_auc = float("nan")
    except (AttributeError, ValueError):
        roc_auc = float("nan")

    tn, fp, fn, tp = confusion_matrix(
        y_test,
        predictions,
        labels=[0, 1],
    ).ravel()

    inference_time_per_sample = (
        inference_time / len(X_test)
    )

    results = {
        "accuracy": float(accuracy),
        "precision": float(precision),
        "recall": float(recall),
        "f1": float(f1),
        "roc_auc": float(roc_auc),
        "true_negatives": int(tn),
        "false_positives": int(fp),
        "false_negatives": int(fn),
        "true_positives": int(tp),
        "total_inference_time_seconds": float(
            inference_time
        ),
        "inference_time_per_sample_seconds": float(
            inference_time_per_sample
        ),
    }

    QUANTUM_RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        QUANTUM_RESULTS_DIR / "vqc_evaluation.csv"
    )

    pd.DataFrame([results]).to_csv(
        output_path,
        index=False,
    )

    print("Phase 15 VQC evaluation completed successfully.")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1: {f1:.4f}")
    print(f"ROC-AUC: {roc_auc:.4f}")
    print(f"True negatives: {tn}")
    print(f"False positives: {fp}")
    print(f"False negatives: {fn}")
    print(f"True positives: {tp}")
    print(
        f"Total inference time: {inference_time:.6f} seconds"
    )
    print(
        "Inference time per sample: "
        f"{inference_time_per_sample * 1000:.6f} ms"
    )
    print(f"Results saved: {output_path}")


if __name__ == "__main__":
    main()