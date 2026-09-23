"""
Phase 16 automated validation tests.

Uses Python's built-in unittest framework.
No external test framework is required.
"""

from __future__ import annotations

import json
import math
import unittest
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RESULTS_DIR = PROJECT_ROOT / "ml" / "comparison" / "results"

COMPARISON_CSV = RESULTS_DIR / "model_comparison.csv"
COMPARISON_JSON = RESULTS_DIR / "model_comparison.json"
METADATA_JSON = RESULTS_DIR / "comparison_metadata.json"


EXPECTED_CLASSICAL_MODELS = {
    "logistic_regression",
    "decision_tree",
    "random_forest",
    "svm",
    "knn",
    "gradient_boosting",
}

EXPECTED_QUANTUM_MODELS = {
    "QSVC",
    "VQC",
}

REQUIRED_COLUMNS = {
    "model",
    "model_family",
    "phase",
    "accuracy",
    "precision",
    "recall",
    "f1",
    "roc_auc",
    "false_positives",
    "false_negatives",
}


class Phase16Tests(unittest.TestCase):
    """Validate Phase 16 comparison artifacts."""

    @classmethod
    def setUpClass(cls) -> None:
        """Load the generated comparison artifacts once."""
        cls.df = pd.read_csv(COMPARISON_CSV)

        with COMPARISON_JSON.open(
            "r",
            encoding="utf-8",
        ) as file:
            cls.comparison_json = json.load(file)

        with METADATA_JSON.open(
            "r",
            encoding="utf-8",
        ) as file:
            cls.metadata = json.load(file)

    def test_01_result_directory_exists(self) -> None:
        """Verify the Phase 16 results directory exists."""
        self.assertTrue(RESULTS_DIR.exists())
        self.assertTrue(RESULTS_DIR.is_dir())

    def test_02_comparison_csv_exists(self) -> None:
        """Verify the unified comparison CSV exists."""
        self.assertTrue(COMPARISON_CSV.exists())
        self.assertGreater(
            COMPARISON_CSV.stat().st_size,
            0,
        )

    def test_03_comparison_json_exists(self) -> None:
        """Verify the comparison JSON exists."""
        self.assertTrue(COMPARISON_JSON.exists())
        self.assertGreater(
            COMPARISON_JSON.stat().st_size,
            0,
        )

    def test_04_metadata_exists(self) -> None:
        """Verify comparison metadata exists."""
        self.assertTrue(METADATA_JSON.exists())
        self.assertGreater(
            METADATA_JSON.stat().st_size,
            0,
        )

    def test_05_required_columns(self) -> None:
        """Verify all required comparison columns exist."""
        missing = REQUIRED_COLUMNS.difference(
            self.df.columns
        )

        self.assertEqual(
            missing,
            set(),
            f"Missing columns: {sorted(missing)}",
        )

    def test_06_expected_model_count(self) -> None:
        """Verify six classical and two quantum models exist."""
        self.assertEqual(
            len(self.df),
            8,
        )

        classical_models = set(
            self.df.loc[
                self.df["model_family"] == "classical",
                "model",
            ]
        )

        quantum_models = set(
            self.df.loc[
                self.df["model_family"] == "quantum",
                "model",
            ]
        )

        self.assertEqual(
            classical_models,
            EXPECTED_CLASSICAL_MODELS,
        )

        self.assertEqual(
            quantum_models,
            EXPECTED_QUANTUM_MODELS,
        )

    def test_07_phase_mapping(self) -> None:
        """Verify model families map to the correct phases."""
        classical_phases = set(
            self.df.loc[
                self.df["model_family"] == "classical",
                "phase",
            ]
        )

        quantum_phases = set(
            self.df.loc[
                self.df["model_family"] == "quantum",
                "phase",
            ]
        )

        self.assertEqual(
            classical_phases,
            {14},
        )

        self.assertEqual(
            quantum_phases,
            {15},
        )

    def test_08_metrics_are_finite(self) -> None:
        """Verify predictive metrics are finite and within 0-1."""
        metric_columns = [
            "accuracy",
            "precision",
            "recall",
            "f1",
            "roc_auc",
        ]

        for column in metric_columns:
            for value in self.df[column]:
                numeric_value = float(value)

                self.assertTrue(
                    math.isfinite(numeric_value),
                    f"{column} contains non-finite value.",
                )

                self.assertGreaterEqual(
                    numeric_value,
                    0.0,
                )

                self.assertLessEqual(
                    numeric_value,
                    1.0,
                )

    def test_09_error_counts_are_valid(self) -> None:
        """Verify false-positive and false-negative counts."""
        for column in [
            "false_positives",
            "false_negatives",
        ]:
            for value in self.df[column]:
                numeric_value = float(value)

                self.assertTrue(
                    math.isfinite(numeric_value)
                )

                self.assertGreaterEqual(
                    numeric_value,
                    0,
                )

                self.assertEqual(
                    numeric_value,
                    int(numeric_value),
                )

    def test_10_models_are_unique(self) -> None:
        """Verify every model appears exactly once."""
        self.assertTrue(
            self.df["model"].is_unique
        )

    def test_11_json_matches_csv(self) -> None:
        """Verify JSON contains the same number of models."""
        self.assertIsInstance(
            self.comparison_json,
            list,
        )

        self.assertEqual(
            len(self.comparison_json),
            len(self.df),
        )

    def test_12_metadata_contract(self) -> None:
        """Verify required Phase 16 metadata fields."""
        self.assertEqual(
            self.metadata["phase"],
            16,
        )

        self.assertEqual(
            self.metadata["experiment"],
            "classical_vs_quantum_model_comparison",
        )

        scope = self.metadata["comparison_scope"]

        self.assertEqual(
            scope["classical_phase"],
            14,
        )

        self.assertEqual(
            scope["quantum_phase"],
            15,
        )

        self.assertTrue(
            scope["phase_13_contract_preserved"]
        )

        self.assertFalse(
            scope["retraining_performed"]
        )

        self.assertFalse(
            scope["test_set_tuning_performed"]
        )

    def test_13_no_quantum_advantage_claim(self) -> None:
        """
        Verify the metadata explicitly documents the
        prohibition on unsupported quantum-advantage claims.
        """
        limitations = self.metadata["limitations"]

        contains_required_statement = any(
            "quantum advantage" in limitation.lower()
            for limitation in limitations
        )

        self.assertTrue(
            contains_required_statement
        )

    def test_14_measured_results_preserved(self) -> None:
        """
        Verify important Phase 14/15 measured values remain
        unchanged in the comparison artifact.
        """
        expected = {
            "logistic_regression": {
                "accuracy": 0.8275862068965517,
                "roc_auc": 0.7681159420289856,
            },
            "gradient_boosting": {
                "accuracy": 0.8275862068965517,
                "roc_auc": 0.9057971014492754,
            },
            "QSVC": {
                "accuracy": 0.7586206896551724,
                "roc_auc": 0.7391304347826086,
            },
            "VQC": {
                "accuracy": 0.6896551724137931,
                "roc_auc": 0.3442028985507246,
            },
        }

        for model_name, metrics in expected.items():
            matching_rows = self.df.loc[
                self.df["model"] == model_name
            ]

            self.assertEqual(
                len(matching_rows),
                1,
            )

            row = matching_rows.iloc[0]

            for metric, expected_value in metrics.items():
                actual_value = float(row[metric])

                self.assertAlmostEqual(
                    actual_value,
                    expected_value,
                    places=12,
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)