import json
import unittest
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]

RESULTS = ROOT / "ml" / "evaluation" / "results"
REPORT = ROOT / "ml" / "evaluation" / "reports" / "PHASE_17_MODEL_EVALUATION_REPORT.md"

EXPECTED_MODELS = {
    "logistic_regression",
    "decision_tree",
    "random_forest",
    "svm",
    "knn",
    "gradient_boosting",
    "qsvc",
    "vqc",
}

EXPECTED_JSON_FILES = {
    "model_evaluation.json",
    "confusion_matrices.json",
    "per_class_metrics.json",
    "roc_pr_data.json",
    "error_analysis.json",
    "evaluation_metadata.json",
}

EXPECTED_CSV_FILES = {
    "model_evaluation.csv",
}


def load_json(filename):
    path = RESULTS / filename

    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def extract_model_names(data):
    if isinstance(data, dict):
        return set(data.keys())

    if isinstance(data, list):
        names = set()

        for item in data:
            if isinstance(item, dict):
                model = item.get("model")

                if model is not None:
                    names.add(model)

        return names

    return set()


class Phase17EvaluationTests(unittest.TestCase):

    def test_results_directory_exists(self):
        self.assertTrue(
            RESULTS.exists(),
            "Phase 17 results directory is missing.",
        )

    def test_report_exists_and_is_non_empty(self):
        self.assertTrue(
            REPORT.exists(),
            "Phase 17 evaluation report is missing.",
        )

        self.assertGreater(
            REPORT.stat().st_size,
            0,
            "Phase 17 evaluation report is empty.",
        )

    def test_expected_json_files_exist(self):
        for filename in EXPECTED_JSON_FILES:
            path = RESULTS / filename

            self.assertTrue(
                path.exists(),
                f"Missing JSON artifact: {filename}",
            )

            self.assertGreater(
                path.stat().st_size,
                0,
                f"Empty JSON artifact: {filename}",
            )

    def test_expected_csv_files_exist(self):
        for filename in EXPECTED_CSV_FILES:
            path = RESULTS / filename

            self.assertTrue(
                path.exists(),
                f"Missing CSV artifact: {filename}",
            )

            self.assertGreater(
                path.stat().st_size,
                0,
                f"Empty CSV artifact: {filename}",
            )

    def test_json_artifacts_are_valid(self):
        for filename in EXPECTED_JSON_FILES:
            data = load_json(filename)

            self.assertIsNotNone(
                data,
                f"JSON artifact contains no data: {filename}",
            )

    def test_evaluation_csv_contains_all_models(self):
        path = RESULTS / "model_evaluation.csv"

        df = pd.read_csv(path)

        self.assertEqual(
            len(df),
            8,
            "Expected exactly 8 evaluated models.",
        )

        self.assertEqual(
            df["model"].nunique(),
            8,
            "Expected 8 unique evaluated models.",
        )

        self.assertEqual(
            set(df["model"]),
            EXPECTED_MODELS,
            "Evaluated model set does not match Phase 17 contract.",
        )

    def test_evaluation_csv_contains_required_metrics(self):
        path = RESULTS / "model_evaluation.csv"

        df = pd.read_csv(path)

        required_columns = {
            "model",
            "accuracy",
            "precision",
            "recall",
            "f1_score",
            "roc_auc",
            "false_positives",
            "false_negatives",
        }

        self.assertTrue(
            required_columns.issubset(df.columns),
            "Required evaluation metric columns are missing.",
        )

    def test_metric_values_are_finite(self):
        path = RESULTS / "model_evaluation.csv"

        df = pd.read_csv(path)

        metric_columns = [
            "accuracy",
            "precision",
            "recall",
            "f1_score",
            "roc_auc",
        ]

        for column in metric_columns:
            self.assertTrue(
                df[column].notna().all(),
                f"Missing metric values detected in {column}.",
            )

            self.assertTrue(
                df[column].map(pd.api.types.is_number).all(),
                f"Non-numeric values detected in {column}.",
            )

    def test_confusion_matrices_contain_all_models(self):
        data = load_json("confusion_matrices.json")
        models = extract_model_names(data)

        self.assertEqual(
            models,
            EXPECTED_MODELS,
            "Confusion-matrix model set does not match Phase 17 contract.",
        )

    def test_per_class_metrics_contain_all_models(self):
        data = load_json("per_class_metrics.json")
        models = extract_model_names(data)

        self.assertEqual(
            models,
            EXPECTED_MODELS,
            "Per-class metric model set does not match Phase 17 contract.",
        )

    def test_error_analysis_contains_all_models(self):
        data = load_json("error_analysis.json")
        models = extract_model_names(data)

        self.assertEqual(
            models,
            EXPECTED_MODELS,
            "Error-analysis model set does not match Phase 17 contract.",
        )

    def test_metadata_contains_phase_information(self):
        data = load_json("evaluation_metadata.json")

        self.assertIsInstance(
            data,
            dict,
            "Evaluation metadata must be a JSON object.",
        )

        self.assertEqual(
            data.get("phase"),
            17,
            "Evaluation metadata must identify Phase 17.",
        )

        self.assertEqual(
            data.get("model_count"),
            8,
            "Evaluation metadata must record eight models.",
        )

    def test_report_contains_required_sections(self):
        content = REPORT.read_text(encoding="utf-8")

        required_sections = [
            "## 1. Evaluation Overview",
            "## 2. Evaluation Contract",
            "## 3. Evaluated Models",
            "## 4. Evaluation Metrics",
            "## 5. Measured Results",
            "## 6. Classical Model Evaluation",
            "## 7. Quantum Model Evaluation",
            "## 8. Inference Characteristics",
            "## 9. Error Analysis",
            "## 10. Confusion Matrices",
            "## 11. Per-Class Evaluation",
            "## 12. ROC and Precision-Recall Evaluation",
            "## 13. Evaluation Metadata",
            "## 14. Reproducibility",
            "## 15. Dataset Limitations",
            "## 16. Interpretation Constraints",
            "## 17. Artifact Inventory",
            "## 18. Phase 18 Handoff",
            "## 19. Phase 17 Completion Criteria",
            "## 20. Conclusion",
        ]

        for section in required_sections:
            self.assertIn(
                section,
                content,
                f"Missing report section: {section}",
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)