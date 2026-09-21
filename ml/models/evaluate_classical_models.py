
from pathlib import Path
import time

import joblib
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

ARTIFACT_DIR = PROJECT_ROOT / "ml" / "preprocessing" / "artifacts"
MODEL_DIR = PROJECT_ROOT / "ml" / "models"

X_TEST_PATH = ARTIFACT_DIR / "X_test.csv"
Y_TEST_PATH = ARTIFACT_DIR / "y_test.csv"

RANDOM_STATE = 42


def load_test_data():
    """Load the untouched Phase 13 test dataset."""
    X_test = pd.read_csv(X_TEST_PATH)
    y_test = pd.read_csv(Y_TEST_PATH).iloc[:, 0]

    return X_test, y_test


def get_model_paths():
    """Return all Phase 14 trained model paths."""
    return {
        "logistic_regression": MODEL_DIR / "logistic_regression.joblib",
        "decision_tree": MODEL_DIR / "decision_tree.joblib",
        "random_forest": MODEL_DIR / "random_forest.joblib",
        "svm": MODEL_DIR / "svm.joblib",
        "knn": MODEL_DIR / "knn.joblib",
        "gradient_boosting": MODEL_DIR / "gradient_boosting.joblib",
    }


def evaluate_model(model_name, model, X_test, y_test):
    """Evaluate one trained model."""
    start_time = time.perf_counter()

    predictions = model.predict(X_test)

    inference_time_sec = time.perf_counter() - start_time
    inference_time_ms_per_sample = (
        inference_time_sec / len(X_test)
    ) * 1000

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
        probabilities = model.predict_proba(X_test)[:, 1]
        roc_auc = roc_auc_score(y_test, probabilities)
    except AttributeError:
        roc_auc = None

    tn, fp, fn, tp = confusion_matrix(
        y_test,
        predictions,
        labels=[0, 1],
    ).ravel()

    return {
        "model": model_name,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "roc_auc": roc_auc,
        "false_positives": int(fp),
        "false_negatives": int(fn),
        "true_negatives": int(tn),
        "true_positives": int(tp),
        "inference_time_sec": inference_time_sec,
        "inference_time_ms_per_sample": inference_time_ms_per_sample,
    }


def main():
    """Run Phase 14 classical ML evaluation."""
    print("=" * 60)
    print("PHASE 14 - CLASSICAL ML EVALUATION")
    print("=" * 60)

    print("\nLoading untouched Phase 13 test data...")
    X_test, y_test = load_test_data()

    print(f"X_test shape: {X_test.shape}")
    print(f"y_test shape: {y_test.shape}")
    print(
        f"Test labels: "
        f"{y_test.value_counts().sort_index().to_dict()}"
    )

    if X_test.isnull().any().any():
        raise ValueError("X_test contains missing values.")

    if y_test.isnull().any():
        raise ValueError("y_test contains missing values.")

    model_paths = get_model_paths()
    results = []

    for model_name, model_path in model_paths.items():
        print(f"\nEvaluating: {model_name}")

        if not model_path.exists():
            raise FileNotFoundError(
                f"Model not found: {model_path}"
            )

        model = joblib.load(model_path)

        result = evaluate_model(
            model_name,
            model,
            X_test,
            y_test,
        )

        results.append(result)

        print(f"  Accuracy: {result['accuracy']:.4f}")
        print(f"  Precision: {result['precision']:.4f}")
        print(f"  Recall: {result['recall']:.4f}")
        print(f"  F1-score: {result['f1_score']:.4f}")

        if result["roc_auc"] is not None:
            print(f"  ROC-AUC: {result['roc_auc']:.4f}")
        else:
            print("  ROC-AUC: unavailable")

        print(
            f"  False positives: "
            f"{result['false_positives']}"
        )
        print(
            f"  False negatives: "
            f"{result['false_negatives']}"
        )
        print(
            f"  Inference time: "
            f"{result['inference_time_sec']:.6f} sec"
        )
        print(
            f"  Inference/sample: "
            f"{result['inference_time_ms_per_sample']:.6f} ms"
        )

    results_df = pd.DataFrame(results)

    output_path = MODEL_DIR / "classical_ml_evaluation.csv"
    results_df.to_csv(output_path, index=False)

    print("\n" + "=" * 60)
    print("EVALUATION SUMMARY")
    print("=" * 60)

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
        ].to_string(index=False)
    )

    print(f"\nSaved evaluation results: {output_path}")
    print("\nPHASE 14 CLASSICAL ML EVALUATION: SUCCESS")


if __name__ == "__main__":
    main()