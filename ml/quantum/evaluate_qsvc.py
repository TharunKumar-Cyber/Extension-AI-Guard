from __future__ import annotations

import time
from pathlib import Path

import joblib
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
    EXPECTED_FEATURE_COUNT,
    EXPECTED_TEST_SAMPLES,
    QUANTUM_KERNEL_MODEL_PATH,
    QUANTUM_RESULTS_DIR,
    X_TEST_PATH,
    Y_TEST_PATH,
)


def load_test_data() -> tuple[np.ndarray, np.ndarray]:
    """Load the frozen Phase 13 test set."""

    x_test = pd.read_csv(X_TEST_PATH).to_numpy(dtype=float)
    y_test = pd.read_csv(Y_TEST_PATH).squeeze("columns").to_numpy(dtype=int)

    if x_test.shape != (EXPECTED_TEST_SAMPLES, EXPECTED_FEATURE_COUNT):
        raise ValueError(
            f"Unexpected X_test shape: {x_test.shape}. "
            f"Expected ({EXPECTED_TEST_SAMPLES}, {EXPECTED_FEATURE_COUNT})."
        )

    if y_test.shape != (EXPECTED_TEST_SAMPLES,):
        raise ValueError(
            f"Unexpected y_test shape: {y_test.shape}. "
            f"Expected ({EXPECTED_TEST_SAMPLES},)."
        )

    if not np.isfinite(x_test).all():
        raise ValueError("X_test contains non-finite values.")

    return x_test, y_test


def evaluate_qsvc() -> dict[str, float | int]:
    """Evaluate the trained QSVC on the untouched Phase 13 test set."""

    x_test, y_test = load_test_data()

    model = joblib.load(QUANTUM_KERNEL_MODEL_PATH)

    print("Phase 15 QSVC evaluation started.")
    print(f"Test samples: {len(x_test)}")
    print(f"Features: {x_test.shape[1]}")
    print(
        "Test labels: "
        f"BENIGN={(y_test == 0).sum()}, "
        f"MALICIOUS={(y_test == 1).sum()}"
    )

    start_time = time.perf_counter()
    predictions = model.predict(x_test)
    total_inference_time = time.perf_counter() - start_time

    decision_scores = model.decision_function(x_test)

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
    roc_auc = roc_auc_score(y_test, decision_scores)

    true_negatives, false_positives, false_negatives, true_positives = (
        confusion_matrix(
            y_test,
            predictions,
            labels=[0, 1],
        ).ravel()
    )

    inference_time_per_sample = (
        total_inference_time / len(x_test)
    )

    results = {
        "accuracy": float(accuracy),
        "precision": float(precision),
        "recall": float(recall),
        "f1": float(f1),
        "roc_auc": float(roc_auc),
        "true_negatives": int(true_negatives),
        "false_positives": int(false_positives),
        "false_negatives": int(false_negatives),
        "true_positives": int(true_positives),
        "total_inference_time_seconds": float(total_inference_time),
        "inference_time_per_sample_seconds": float(
            inference_time_per_sample
        ),
    }

    QUANTUM_RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    output_path = QUANTUM_RESULTS_DIR / "qsvc_evaluation.csv"

    pd.DataFrame([results]).to_csv(
        output_path,
        index=False,
    )

    print("Phase 15 QSVC evaluation completed successfully.")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1: {f1:.4f}")
    print(f"ROC-AUC: {roc_auc:.4f}")
    print(f"True negatives: {true_negatives}")
    print(f"False positives: {false_positives}")
    print(f"False negatives: {false_negatives}")
    print(f"True positives: {true_positives}")
    print(f"Total inference time: {total_inference_time:.6f} seconds")
    print(
        "Inference time per sample: "
        f"{inference_time_per_sample * 1000:.6f} ms"
    )
    print(f"Results saved: {output_path}")

    return results


if __name__ == "__main__":
    evaluate_qsvc()