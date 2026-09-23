from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import cloudpickle
import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PREPROCESSING_DIR = PROJECT_ROOT / "ml" / "preprocessing" / "artifacts"
CLASSICAL_DIR = PROJECT_ROOT / "ml" / "models"
QUANTUM_DIR = PROJECT_ROOT / "ml" / "quantum"
EVALUATION_DIR = PROJECT_ROOT / "ml" / "evaluation"

RESULTS_DIR = EVALUATION_DIR / "results"

X_TEST_PATH = PREPROCESSING_DIR / "X_test.csv"
Y_TEST_PATH = PREPROCESSING_DIR / "y_test.csv"

CLASSICAL_MODELS = {
    "logistic_regression": CLASSICAL_DIR / "logistic_regression.joblib",
    "decision_tree": CLASSICAL_DIR / "decision_tree.joblib",
    "random_forest": CLASSICAL_DIR / "random_forest.joblib",
    "svm": CLASSICAL_DIR / "svm.joblib",
    "knn": CLASSICAL_DIR / "knn.joblib",
    "gradient_boosting": CLASSICAL_DIR / "gradient_boosting.joblib",
}

QSVC_PATH = (
    QUANTUM_DIR
    / "artifacts"
    / "quantum_kernel"
    / "qsvc_model.joblib"
)

VQC_PATH = (
    QUANTUM_DIR
    / "artifacts"
    / "vqc"
    / "vqc_model.joblib"
)

EXPECTED_TEST_SAMPLES = 29
EXPECTED_FEATURE_COUNT = 8
RANDOM_STATE = 42
EXPECTED_MODELS = 8


def make_json_safe(value):
    """Recursively convert non-finite values to JSON-safe values."""

    if isinstance(value, (float, np.floating)):
        value = float(value)

        if np.isfinite(value):
            return value

        return None

    if isinstance(value, (int, np.integer)):
        return int(value)

    if isinstance(value, dict):
        return {
            str(key): make_json_safe(item)
            for key, item in value.items()
        }

    if isinstance(value, (list, tuple)):
        return [
            make_json_safe(item)
            for item in value
        ]

    if isinstance(value, np.ndarray):
        return [
            make_json_safe(item)
            for item in value.tolist()
        ]

    return value


def load_test_data() -> tuple[np.ndarray, np.ndarray]:
    """Load and validate the frozen Phase 13 test artifacts."""

    if not X_TEST_PATH.exists():
        raise FileNotFoundError(
            f"Missing X_test artifact: {X_TEST_PATH}"
        )

    if not Y_TEST_PATH.exists():
        raise FileNotFoundError(
            f"Missing y_test artifact: {Y_TEST_PATH}"
        )

    X_test = pd.read_csv(
        X_TEST_PATH
    ).to_numpy(dtype=float)

    y_test = (
        pd.read_csv(Y_TEST_PATH)
        .iloc[:, 0]
        .to_numpy(dtype=int)
    )

    if X_test.shape != (
        EXPECTED_TEST_SAMPLES,
        EXPECTED_FEATURE_COUNT,
    ):
        raise ValueError(
            f"Unexpected X_test shape: {X_test.shape}. "
            f"Expected ({EXPECTED_TEST_SAMPLES}, "
            f"{EXPECTED_FEATURE_COUNT})."
        )

    if y_test.shape != (
        EXPECTED_TEST_SAMPLES,
    ):
        raise ValueError(
            f"Unexpected y_test shape: {y_test.shape}. "
            f"Expected ({EXPECTED_TEST_SAMPLES},)."
        )

    if not np.isfinite(X_test).all():
        raise ValueError(
            "X_test contains non-finite values."
        )

    if not np.isin(
        y_test,
        [0, 1],
    ).all():
        raise ValueError(
            "y_test contains labels outside {0, 1}."
        )

    if int(
        (y_test == 0).sum()
    ) != 23:
        raise ValueError(
            "Expected 23 BENIGN test samples."
        )

    if int(
        (y_test == 1).sum()
    ) != 6:
        raise ValueError(
            "Expected 6 MALICIOUS test samples."
        )

    return X_test, y_test


def load_model(
    model_name: str,
    model_path: Path,
):
    """Load one Phase 14 or Phase 15 saved model."""

    if not model_path.exists():
        raise FileNotFoundError(
            f"Missing model artifact for "
            f"{model_name}: {model_path}"
        )

    if model_name == "vqc":
        with open(
            model_path,
            "rb",
        ) as model_file:
            return cloudpickle.load(
                model_file
            )

    return joblib.load(
        model_path
    )


def get_score_vector(
    model,
    X_test: np.ndarray,
) -> tuple[np.ndarray | None, str]:
    """
    Obtain a malicious-class score for ROC/PR analysis.

    Priority:
    1. predict_proba
    2. decision_function
    """

    if hasattr(
        model,
        "predict_proba",
    ):
        try:
            probabilities = np.asarray(
                model.predict_proba(
                    X_test
                )
            )

            if (
                probabilities.ndim == 2
                and probabilities.shape[1] >= 2
            ):
                return (
                    probabilities[:, 1].astype(float),
                    "predict_proba",
                )

        except (
            AttributeError,
            ValueError,
            TypeError,
        ):
            pass

    if hasattr(
        model,
        "decision_function",
    ):
        try:
            scores = np.asarray(
                model.decision_function(
                    X_test
                )
            ).reshape(-1)

            if (
                scores.shape[0]
                == X_test.shape[0]
            ):
                return (
                    scores.astype(float),
                    "decision_function",
                )

        except (
            AttributeError,
            ValueError,
            TypeError,
        ):
            pass

    return None, "unavailable"


def evaluate_model(
    model_name: str,
    model,
    X_test: np.ndarray,
    y_test: np.ndarray,
) -> tuple[
    dict,
    dict,
    dict | None,
    list[dict],
]:
    """Evaluate one saved model without retraining."""

    start_time = time.perf_counter()

    predictions = np.asarray(
        model.predict(
            X_test
        )
    ).reshape(-1)

    inference_time = (
        time.perf_counter()
        - start_time
    )

    predictions = predictions.astype(
        int
    )

    if predictions.shape != y_test.shape:
        raise ValueError(
            f"{model_name}: prediction shape "
            f"{predictions.shape} does not match "
            f"test shape {y_test.shape}."
        )

    if not np.isin(
        predictions,
        [0, 1],
    ).all():
        raise ValueError(
            f"{model_name}: predictions contain "
            f"labels outside {{0, 1}}."
        )

    score_vector, score_source = (
        get_score_vector(
            model,
            X_test,
        )
    )

    accuracy = accuracy_score(
        y_test,
        predictions,
    )

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

    tn, fp, fn, tp = confusion_matrix(
        y_test,
        predictions,
        labels=[0, 1],
    ).ravel()

    specificity = (
        tn / (tn + fp)
        if (tn + fp) > 0
        else 0.0
    )

    if score_vector is not None:

        if not np.isfinite(
            score_vector
        ).all():
            raise ValueError(
                f"{model_name}: score vector "
                f"contains non-finite values."
            )

        roc_auc = roc_auc_score(
            y_test,
            score_vector,
        )

        average_precision = (
            average_precision_score(
                y_test,
                score_vector,
            )
        )

    else:
        roc_auc = None
        average_precision = None

    report = classification_report(
        y_test,
        predictions,
        labels=[0, 1],
        target_names=[
            "BENIGN",
            "MALICIOUS",
        ],
        output_dict=True,
        zero_division=0,
    )

    result = {
        "model": model_name,
        "phase": (
            "14"
            if model_name in CLASSICAL_MODELS
            else "15"
        ),
        "model_family": (
            "classical"
            if model_name in CLASSICAL_MODELS
            else "quantum"
        ),
        "accuracy": float(
            accuracy
        ),
        "precision": float(
            precision
        ),
        "recall": float(
            recall
        ),
        "f1_score": float(
            f1
        ),
        "specificity": float(
            specificity
        ),
        "roc_auc": (
            float(roc_auc)
            if roc_auc is not None
            else None
        ),
        "average_precision": (
            float(
                average_precision
            )
            if average_precision is not None
            else None
        ),
        "true_negatives": int(tn),
        "false_positives": int(fp),
        "false_negatives": int(fn),
        "true_positives": int(tp),
        "inference_time_seconds": float(
            inference_time
        ),
        "inference_time_ms_per_sample": float(
            (
                inference_time
                / len(X_test)
            )
            * 1000
        ),
        "score_source": score_source,
    }

    confusion = {
        "model": model_name,
        "true_negatives": int(tn),
        "false_positives": int(fp),
        "false_negatives": int(fn),
        "true_positives": int(tp),
    }

    per_class = {
        "model": model_name,
        "BENIGN": {
            "precision": float(
                report["BENIGN"]["precision"]
            ),
            "recall": float(
                report["BENIGN"]["recall"]
            ),
            "f1_score": float(
                report["BENIGN"]["f1-score"]
            ),
            "support": int(
                report["BENIGN"]["support"]
            ),
        },
        "MALICIOUS": {
            "precision": float(
                report["MALICIOUS"]["precision"]
            ),
            "recall": float(
                report["MALICIOUS"]["recall"]
            ),
            "f1_score": float(
                report["MALICIOUS"]["f1-score"]
            ),
            "support": int(
                report["MALICIOUS"]["support"]
            ),
        },
    }

    curve_data = None

    if score_vector is not None:

        fpr, tpr, roc_thresholds = (
            roc_curve(
                y_test,
                score_vector,
            )
        )

        (
            pr_precision,
            pr_recall,
            pr_thresholds,
        ) = precision_recall_curve(
            y_test,
            score_vector,
        )

        curve_data = {
            "model": model_name,
            "score_source": score_source,
            "roc": {
                "fpr": [
                    float(value)
                    for value in fpr
                ],
                "tpr": [
                    float(value)
                    for value in tpr
                ],
                "thresholds": [
                    (
                        float(value)
                        if np.isfinite(value)
                        else None
                    )
                    for value in roc_thresholds
                ],
            },
            "precision_recall": {
                "precision": [
                    float(value)
                    for value in pr_precision
                ],
                "recall": [
                    float(value)
                    for value in pr_recall
                ],
                "thresholds": [
                    (
                        float(value)
                        if np.isfinite(value)
                        else None
                    )
                    for value in pr_thresholds
                ],
            },
        }

    errors = []

    for index, (
        actual,
        predicted,
    ) in enumerate(
        zip(
            y_test,
            predictions,
        )
    ):

        if int(actual) != int(
            predicted
        ):

            error = {
                "model": model_name,
                "test_index": int(
                    index
                ),
                "actual_label": (
                    "MALICIOUS"
                    if int(actual) == 1
                    else "BENIGN"
                ),
                "predicted_label": (
                    "MALICIOUS"
                    if int(predicted) == 1
                    else "BENIGN"
                ),
                "error_type": (
                    "false_positive"
                    if int(actual) == 0
                    else "false_negative"
                ),
            }

            if score_vector is not None:
                error["score"] = float(
                    score_vector[index]
                )

            errors.append(
                error
            )

    return (
        result,
        per_class,
        curve_data,
        errors,
    )


def build_metadata(
    X_test: np.ndarray,
    y_test: np.ndarray,
) -> dict:
    """Build Phase 17 reproducibility metadata."""

    return {
        "phase": 17,
        "experiment": (
            "Formal model evaluation"
        ),
        "timestamp_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "dataset_contract": {
            "source": (
                "Phase 13 frozen "
                "processed test set"
            ),
            "test_samples": int(
                len(X_test)
            ),
            "feature_count": int(
                X_test.shape[1]
            ),
            "benign_samples": int(
                (y_test == 0).sum()
            ),
            "malicious_samples": int(
                (y_test == 1).sum()
            ),
            "label_mapping": {
                "BENIGN": 0,
                "MALICIOUS": 1,
            },
            "random_state": RANDOM_STATE,
        },
        "evaluation_policy": {
            "retraining": False,
            "test_set_tuning": False,
            "test_set_modification": False,
            "phase_13_preprocessing_reused": True,
        },
        "software": {
            "python": sys.version.split()[0],
            "numpy": np.__version__,
            "pandas": pd.__version__,
            "scikit_learn": sklearn.__version__,
        },
        "model_count": EXPECTED_MODELS,
        "models": [
            "logistic_regression",
            "decision_tree",
            "random_forest",
            "svm",
            "knn",
            "gradient_boosting",
            "qsvc",
            "vqc",
        ],
    }


def main() -> None:
    """Run the complete Phase 17 evaluation."""

    print("=" * 70)
    print(
        "PHASE 17 - FORMAL MODEL EVALUATION"
    )
    print("=" * 70)

    X_test, y_test = load_test_data()

    print("\nFrozen Phase 13 test set:")
    print(
        f"  Samples: {len(X_test)}"
    )
    print(
        f"  Features: {X_test.shape[1]}"
    )
    print(
        f"  BENIGN: {(y_test == 0).sum()}"
    )
    print(
        f"  MALICIOUS: {(y_test == 1).sum()}"
    )

    models = {}

    for (
        model_name,
        model_path,
    ) in CLASSICAL_MODELS.items():

        models[model_name] = load_model(
            model_name,
            model_path,
        )

    models["qsvc"] = load_model(
        "qsvc",
        QSVC_PATH,
    )

    models["vqc"] = load_model(
        "vqc",
        VQC_PATH,
    )

    results = []
    per_class_results = []
    confusion_results = []
    curve_results = []
    error_results = []

    for (
        model_name,
        model,
    ) in models.items():

        print(
            f"\nEvaluating {model_name}..."
        )

        (
            result,
            per_class,
            curves,
            errors,
        ) = evaluate_model(
            model_name,
            model,
            X_test,
            y_test,
        )

        results.append(
            result
        )

        per_class_results.append(
            per_class
        )

        confusion_results.append(
            {
                "model": model_name,
                "true_negatives": result[
                    "true_negatives"
                ],
                "false_positives": result[
                    "false_positives"
                ],
                "false_negatives": result[
                    "false_negatives"
                ],
                "true_positives": result[
                    "true_positives"
                ],
            }
        )

        if curves is not None:
            curve_results.append(
                curves
            )

        error_results.extend(
            errors
        )

        print(
            f"  Accuracy: "
            f"{result['accuracy']:.4f}"
        )

        print(
            f"  Precision: "
            f"{result['precision']:.4f}"
        )

        print(
            f"  Recall: "
            f"{result['recall']:.4f}"
        )

        print(
            f"  F1: "
            f"{result['f1_score']:.4f}"
        )

        if result["roc_auc"] is not None:
            print(
                f"  ROC-AUC: "
                f"{result['roc_auc']:.4f}"
            )
        else:
            print(
                "  ROC-AUC: unavailable"
            )

        print(
            f"  FP: "
            f"{result['false_positives']}"
        )

        print(
            f"  FN: "
            f"{result['false_negatives']}"
        )

        print(
            "  Inference/sample: "
            f"{result['inference_time_ms_per_sample']:.6f} ms"
        )

    if len(results) != EXPECTED_MODELS:
        raise RuntimeError(
            f"Expected {EXPECTED_MODELS} models, "
            f"evaluated {len(results)}."
        )

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    results_df = pd.DataFrame(
        results
    )

    results_df.to_csv(
        RESULTS_DIR
        / "model_evaluation.csv",
        index=False,
    )

    safe_results = make_json_safe(
        results
    )

    safe_confusion_results = (
        make_json_safe(
            confusion_results
        )
    )

    safe_per_class_results = (
        make_json_safe(
            per_class_results
        )
    )

    safe_curve_results = (
        make_json_safe(
            curve_results
        )
    )

    safe_error_results = (
        make_json_safe(
            error_results
        )
    )

    (
        RESULTS_DIR
        / "model_evaluation.json"
    ).write_text(
        json.dumps(
            safe_results,
            indent=2,
            allow_nan=False,
        ),
        encoding="utf-8",
    )

    (
        RESULTS_DIR
        / "confusion_matrices.json"
    ).write_text(
        json.dumps(
            safe_confusion_results,
            indent=2,
            allow_nan=False,
        ),
        encoding="utf-8",
    )

    (
        RESULTS_DIR
        / "per_class_metrics.json"
    ).write_text(
        json.dumps(
            safe_per_class_results,
            indent=2,
            allow_nan=False,
        ),
        encoding="utf-8",
    )

    (
        RESULTS_DIR
        / "roc_pr_data.json"
    ).write_text(
        json.dumps(
            safe_curve_results,
            indent=2,
            allow_nan=False,
        ),
        encoding="utf-8",
    )

    (
        RESULTS_DIR
        / "error_analysis.json"
    ).write_text(
        json.dumps(
            safe_error_results,
            indent=2,
            allow_nan=False,
        ),
        encoding="utf-8",
    )

    metadata = build_metadata(
        X_test,
        y_test,
    )

    safe_metadata = make_json_safe(
        metadata
    )

    (
        RESULTS_DIR
        / "evaluation_metadata.json"
    ).write_text(
        json.dumps(
            safe_metadata,
            indent=2,
            allow_nan=False,
        ),
        encoding="utf-8",
    )

    print(
        "\n" + "=" * 70
    )
    print(
        "PHASE 17 EVALUATION SUMMARY"
    )
    print(
        "=" * 70
    )

    print(
        results_df[
            [
                "model",
                "accuracy",
                "precision",
                "recall",
                "f1_score",
                "roc_auc",
                "false_positives",
                "false_negatives",
            ]
        ].to_string(
            index=False
        )
    )

    print("\nSaved results:")

    print(
        RESULTS_DIR
        / "model_evaluation.csv"
    )

    print(
        RESULTS_DIR
        / "model_evaluation.json"
    )

    print(
        RESULTS_DIR
        / "confusion_matrices.json"
    )

    print(
        RESULTS_DIR
        / "per_class_metrics.json"
    )

    print(
        RESULTS_DIR
        / "roc_pr_data.json"
    )

    print(
        RESULTS_DIR
        / "error_analysis.json"
    )

    print(
        RESULTS_DIR
        / "evaluation_metadata.json"
    )

    print(
        "\nPHASE 17 MODEL EVALUATION: SUCCESS"
    )


if __name__ == "__main__":
    main()