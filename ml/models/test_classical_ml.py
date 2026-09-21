from pathlib import Path
import json

import joblib
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_DIR = PROJECT_ROOT / "ml" / "models"
ARTIFACT_DIR = PROJECT_ROOT / "ml" / "preprocessing" / "artifacts"


EXPECTED_MODELS = [
    "logistic_regression",
    "decision_tree",
    "random_forest",
    "svm",
    "knn",
    "gradient_boosting",
]


def test_model_artifacts_exist():
    for model_name in EXPECTED_MODELS:
        model_path = MODEL_DIR / f"{model_name}.joblib"
        assert model_path.exists(), f"Missing model: {model_path}"
        assert model_path.stat().st_size > 0, f"Empty model: {model_path}"


def test_model_artifacts_load():
    for model_name in EXPECTED_MODELS:
        model_path = MODEL_DIR / f"{model_name}.joblib"
        model = joblib.load(model_path)
        assert model is not None


def test_preprocessing_artifacts_exist():
    required_files = [
        "X_train.csv",
        "X_test.csv",
        "y_train.csv",
        "y_test.csv",
        "preprocessor.joblib",
        "label_mapping.csv",
        "feature_metadata.csv",
    ]

    for filename in required_files:
        path = ARTIFACT_DIR / filename
        assert path.exists(), f"Missing preprocessing artifact: {path}"
        assert path.stat().st_size > 0, f"Empty preprocessing artifact: {path}"


def test_training_and_testing_shapes():
    X_train = pd.read_csv(ARTIFACT_DIR / "X_train.csv")
    X_test = pd.read_csv(ARTIFACT_DIR / "X_test.csv")
    y_train = pd.read_csv(ARTIFACT_DIR / "y_train.csv")
    y_test = pd.read_csv(ARTIFACT_DIR / "y_test.csv")

    assert X_train.shape == (115, 8)
    assert X_test.shape == (29, 8)
    assert len(y_train) == 115
    assert len(y_test) == 29


def test_processed_data_has_no_missing_values():
    X_train = pd.read_csv(ARTIFACT_DIR / "X_train.csv")
    X_test = pd.read_csv(ARTIFACT_DIR / "X_test.csv")

    assert not X_train.isnull().any().any()
    assert not X_test.isnull().any().any()


def test_evaluation_artifact():
    evaluation_path = MODEL_DIR / "classical_ml_evaluation.csv"
    evaluation = pd.read_csv(evaluation_path)

    assert len(evaluation) == 6
    assert set(evaluation["model"]) == set(EXPECTED_MODELS)

    required_columns = [
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

    for column in required_columns:
        assert column in evaluation.columns


def test_baseline_metrics_artifact():
    baseline_path = MODEL_DIR / "baseline_metrics.json"

    with baseline_path.open("r", encoding="utf-8") as file:
        baseline = json.load(file)

    assert baseline["phase"] == 14
    assert baseline["random_state"] == 42
    assert baseline["training_samples"] == 115
    assert baseline["test_samples"] == 29
    assert baseline["processed_features"] == 8

    assert baseline["label_mapping"] == {
        "BENIGN": 0,
        "MALICIOUS": 1,
    }

    assert len(baseline["models"]) == 6

    model_names = {
        model["model"]
        for model in baseline["models"]
    }

    assert model_names == set(EXPECTED_MODELS)


def test_baseline_metrics_match_evaluation():
    evaluation = pd.read_csv(
        MODEL_DIR / "classical_ml_evaluation.csv"
    )

    with (
        MODEL_DIR / "baseline_metrics.json"
    ).open("r", encoding="utf-8") as file:
        baseline = json.load(file)

    baseline_by_model = {
        item["model"]: item["metrics"]
        for item in baseline["models"]
    }

    for _, row in evaluation.iterrows():
        model_name = row["model"]
        metrics = baseline_by_model[model_name]

        assert metrics["accuracy"] == row["accuracy"]
        assert metrics["precision"] == row["precision"]
        assert metrics["recall"] == row["recall"]
        assert metrics["f1_score"] == row["f1_score"]
        assert metrics["roc_auc"] == row["roc_auc"]


def test_training_benchmarks_present():
    with (
        MODEL_DIR / "baseline_metrics.json"
    ).open("r", encoding="utf-8") as file:
        baseline = json.load(file)

    for model in baseline["models"]:
        metrics = model["metrics"]

        assert metrics["train_time_sec"] >= 0
        assert metrics["inference_time_sec"] >= 0
        assert metrics["inference_time_ms_per_sample"] >= 0


def test_confusion_matrix_counts_are_consistent():
    evaluation = pd.read_csv(
        MODEL_DIR / "classical_ml_evaluation.csv"
    )

    for _, row in evaluation.iterrows():
        total = (
            row["true_negatives"]
            + row["true_positives"]
            + row["false_negatives"]
            + row["false_positives"]
        )

        assert total == 29


def run_tests():
    tests = [
        test_model_artifacts_exist,
        test_model_artifacts_load,
        test_preprocessing_artifacts_exist,
        test_training_and_testing_shapes,
        test_processed_data_has_no_missing_values,
        test_evaluation_artifact,
        test_baseline_metrics_artifact,
        test_baseline_metrics_match_evaluation,
        test_training_benchmarks_present,
        test_confusion_matrix_counts_are_consistent,
    ]

    passed = 0

    print("=" * 60)
    print("PHASE 14 - CLASSICAL ML AUTOMATED TESTS")
    print("=" * 60)

    for test in tests:
        test()
        passed += 1
        print(f"PASS: {test.__name__}")

    print()
    print(f"ALL TESTS PASSED: {passed}/{len(tests)}")


if __name__ == "__main__":
    run_tests()