from pathlib import Path
import json
from datetime import datetime, timezone

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_DIR = PROJECT_ROOT / "ml" / "models"

EVALUATION_PATH = MODEL_DIR / "classical_ml_evaluation.csv"
OUTPUT_PATH = MODEL_DIR / "baseline_metrics.json"


TRAINING_TIMES = {
    "logistic_regression": 0.036843,
    "decision_tree": 0.002781,
    "random_forest": 0.094974,
    "svm": 0.038528,
    "knn": 0.002460,
    "gradient_boosting": 0.074427,
}


def main():
    """Generate the unified Phase 14 baseline metrics artifact."""
    print("=" * 60)
    print("PHASE 14 - BASELINE METRICS GENERATION")
    print("=" * 60)

    if not EVALUATION_PATH.exists():
        raise FileNotFoundError(
            f"Evaluation file not found: {EVALUATION_PATH}"
        )

    evaluation_df = pd.read_csv(EVALUATION_PATH)

    required_columns = [
        "model",
        "accuracy",
        "precision",
        "recall",
        "f1_score",
        "roc_auc",
        "false_positives",
        "false_negatives",
        "true_negatives",
        "true_positives",
        "inference_time_sec",
        "inference_time_ms_per_sample",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in evaluation_df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing evaluation columns: {missing_columns}"
        )

    models = []

    for _, row in evaluation_df.iterrows():
        model_name = row["model"]

        if model_name not in TRAINING_TIMES:
            raise ValueError(
                f"Missing training benchmark for model: {model_name}"
            )

        model_metrics = {
            "accuracy": float(row["accuracy"]),
            "precision": float(row["precision"]),
            "recall": float(row["recall"]),
            "f1_score": float(row["f1_score"]),
            "roc_auc": float(row["roc_auc"]),
            "false_positives": int(row["false_positives"]),
            "false_negatives": int(row["false_negatives"]),
            "true_negatives": int(row["true_negatives"]),
            "true_positives": int(row["true_positives"]),
            "train_time_sec": TRAINING_TIMES[model_name],
            "inference_time_sec": float(
                row["inference_time_sec"]
            ),
            "inference_time_ms_per_sample": float(
                row["inference_time_ms_per_sample"]
            ),
        }

        models.append(
            {
                "model": model_name,
                "metrics": model_metrics,
            }
        )

    baseline = {
        "phase": 14,
        "artifact": "classical_ml_baseline_metrics",
        "generated_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "random_state": 42,
        "test_samples": 29,
        "training_samples": 115,
        "processed_features": 8,
        "label_mapping": {
            "BENIGN": 0,
            "MALICIOUS": 1,
        },
        "models": models,
    }

    OUTPUT_PATH.write_text(
        json.dumps(
            baseline,
            indent=4,
        ),
        encoding="utf-8",
    )

    print(f"\nModels included: {len(models)}")
    print(f"Saved baseline metrics: {OUTPUT_PATH}")
    print("\nPHASE 14 BASELINE METRICS: SUCCESS")


if __name__ == "__main__":
    main()