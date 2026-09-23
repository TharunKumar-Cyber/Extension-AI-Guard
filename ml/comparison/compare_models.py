"""
Phase 16 - Classical vs Quantum Model Comparison

Consumes existing Phase 14 and Phase 15 evaluation artifacts.
No model retraining is performed in this module.
"""

from __future__ import annotations

import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

PHASE14_RESULTS = PROJECT_ROOT / "ml" / "models"
PHASE15_RESULTS = PROJECT_ROOT / "ml" / "quantum" / "results"

OUTPUT_DIR = PROJECT_ROOT / "ml" / "comparison" / "results"

COMPARISON_CSV = OUTPUT_DIR / "model_comparison.csv"
COMPARISON_JSON = OUTPUT_DIR / "model_comparison.json"
METADATA_JSON = OUTPUT_DIR / "comparison_metadata.json"


REQUIRED_METRICS = [
    "accuracy",
    "precision",
    "recall",
    "f1",
    "roc_auc",
    "false_positives",
    "false_negatives",
]


def utc_timestamp() -> str:
    """Return the current UTC timestamp."""
    return datetime.now(timezone.utc).isoformat()


def find_result_file(directory: Path, filename: str) -> Path:
    """
    Find a result file recursively.

    Raises:
        FileNotFoundError: If the expected file cannot be found.
    """
    candidates = list(directory.rglob(filename))

    if not candidates:
        raise FileNotFoundError(
            f"Could not find '{filename}' under '{directory}'."
        )

    return candidates[0]


def normalize_column_name(name: str) -> str:
    """Normalize a column name for matching."""
    return (
        str(name)
        .strip()
        .lower()
        .replace("-", "_")
        .replace(" ", "_")
    )


def normalize_dataframe_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize dataframe column names."""
    renamed = {
        column: normalize_column_name(column)
        for column in df.columns
    }
    return df.rename(columns=renamed)


def load_csv_result(
    path: Path,
    source_phase: int,
) -> pd.DataFrame:
    """
    Load and normalize a model evaluation CSV.

    The function supports either:
    - one row per model, or
    - one row representing a single model.
    """
    df = pd.read_csv(path)

    if df.empty:
        raise ValueError(f"Result file is empty: {path}")

    df = normalize_dataframe_columns(df)
    df["source_phase"] = source_phase
    df["source_file"] = str(path.relative_to(PROJECT_ROOT))

    return df


def locate_phase14_results() -> Path:
    """Locate the Phase 14 classical evaluation results."""
    preferred_names = [
        "classical_ml_evaluation.csv",
        "model_evaluation.csv",
        "classical_model_evaluation.csv",
        "evaluation_results.csv",
    ]

    for filename in preferred_names:
        try:
            return find_result_file(PHASE14_RESULTS, filename)
        except FileNotFoundError:
            continue

    csv_files = list(PHASE14_RESULTS.rglob("*.csv"))

    if len(csv_files) == 1:
        return csv_files[0]

    raise FileNotFoundError(
        "Unable to identify the Phase 14 classical evaluation CSV. "
        f"Checked directory: {PHASE14_RESULTS}"
    )


def locate_phase15_results() -> Path:
    """Locate the Phase 15 unified quantum evaluation results."""
    preferred_names = [
        "quantum_ml_evaluation.csv",
    ]

    for filename in preferred_names:
        try:
            return find_result_file(PHASE15_RESULTS, filename)
        except FileNotFoundError:
            continue

    raise FileNotFoundError(
        "Unable to locate the Phase 15 quantum evaluation CSV. "
        f"Expected under: {PHASE15_RESULTS}"
    )


def identify_model_column(df: pd.DataFrame) -> str:
    """Identify the model-name column."""
    candidates = [
        "model",
        "model_name",
        "classifier",
        "algorithm",
        "model_type",
    ]

    for candidate in candidates:
        if candidate in df.columns:
            return candidate

    raise ValueError(
        "Could not identify a model column. "
        f"Available columns: {list(df.columns)}"
    )


def identify_metric_column(
    df: pd.DataFrame,
    metric: str,
) -> str | None:
    """Identify a requested metric column."""
    aliases = {
        "accuracy": [
            "accuracy",
            "accuracy_score",
        ],
        "precision": [
            "precision",
            "precision_score",
        ],
        "recall": [
            "recall",
            "recall_score",
        ],
        "f1": [
            "f1",
            "f1_score",
            "f1score",
        ],
        "roc_auc": [
            "roc_auc",
            "roc_auc_score",
            "rocauc",
        ],
        "false_positives": [
            "false_positives",
            "false_positive",
            "fp",
        ],
        "false_negatives": [
            "false_negatives",
            "false_negative",
            "fn",
        ],
    }

    for candidate in aliases[metric]:
        if candidate in df.columns:
            return candidate

    return None


def convert_to_comparison_rows(
    df: pd.DataFrame,
    phase: int,
) -> list[dict[str, Any]]:
    """Convert an evaluation dataframe into standardized comparison rows."""
    model_column = identify_model_column(df)

    rows: list[dict[str, Any]] = []

    for _, source_row in df.iterrows():
        model_name = str(source_row[model_column])

        row: dict[str, Any] = {
            "model": model_name,
            "phase": phase,
        }

        for metric in REQUIRED_METRICS:
            column = identify_metric_column(df, metric)

            if column is None:
                row[metric] = None
            else:
                value = source_row[column]

                if pd.isna(value):
                    row[metric] = None
                elif metric in {"false_positives", "false_negatives"}:
                    row[metric] = int(value)
                else:
                    row[metric] = float(value)

        rows.append(row)

    return rows


def add_model_family(rows: list[dict[str, Any]]) -> None:
    """Add classical/quantum family labels."""
    for row in rows:
        phase = int(row["phase"])

        if phase == 14:
            row["model_family"] = "classical"
        elif phase == 15:
            row["model_family"] = "quantum"
        else:
            row["model_family"] = "unknown"


def validate_rows(rows: list[dict[str, Any]]) -> None:
    """Validate the standardized comparison rows."""
    if not rows:
        raise ValueError("No model comparison rows were generated.")

    for row in rows:
        for key in [
            "model",
            "phase",
            "model_family",
        ]:
            if key not in row:
                raise ValueError(
                    f"Missing required comparison field '{key}'."
                )

        for metric in REQUIRED_METRICS:
            if metric not in row:
                raise ValueError(
                    f"Missing metric '{metric}' for model "
                    f"{row['model']}."
                )


def create_comparison_dataframe(
    rows: list[dict[str, Any]],
) -> pd.DataFrame:
    """Create the final comparison dataframe."""
    columns = [
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
    ]

    df = pd.DataFrame(rows)

    for column in columns:
        if column not in df.columns:
            df[column] = None

    return df[columns]


def build_metadata(
    phase14_path: Path,
    phase15_path: Path,
    comparison_df: pd.DataFrame,
) -> dict[str, Any]:
    """Build reproducibility metadata."""
    return {
        "phase": 16,
        "experiment": "classical_vs_quantum_model_comparison",
        "generated_at_utc": utc_timestamp(),
        "project": "Extension AI Guard",
        "comparison_scope": {
            "classical_phase": 14,
            "quantum_phase": 15,
            "phase_13_contract_preserved": True,
            "retraining_performed": False,
            "test_set_tuning_performed": False,
        },
        "input_artifacts": {
            "phase_14_results": str(
                phase14_path.relative_to(PROJECT_ROOT)
            ),
            "phase_15_results": str(
                phase15_path.relative_to(PROJECT_ROOT)
            ),
        },
        "model_count": int(len(comparison_df)),
        "classical_model_count": int(
            (comparison_df["model_family"] == "classical").sum()
        ),
        "quantum_model_count": int(
            (comparison_df["model_family"] == "quantum").sum()
        ),
        "python_version": sys.version,
        "python_implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "random_state": 42,
        "limitations": [
            "Phase 16 uses the small Phase 13 dataset.",
            "The Phase 13 test set contains only 29 samples.",
            "Only six malicious test samples are available.",
            "Observed results do not establish quantum advantage.",
            "Runtime measurements are configuration-dependent.",
            "Phase 16 does not select a production model.",
        ],
    }


def save_outputs(
    comparison_df: pd.DataFrame,
    metadata: dict[str, Any],
) -> None:
    """Save CSV and JSON comparison artifacts."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    comparison_df.to_csv(
        COMPARISON_CSV,
        index=False,
    )

    comparison_records = comparison_df.to_dict(
        orient="records"
    )

    with COMPARISON_JSON.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            comparison_records,
            file,
            indent=2,
        )

    with METADATA_JSON.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            metadata,
            file,
            indent=2,
        )


def main() -> None:
    """Run Phase 16 classical-vs-quantum comparison."""
    print("=" * 70)
    print("Extension AI Guard - Phase 16 Model Comparison")
    print("=" * 70)

    phase14_path = locate_phase14_results()
    phase15_path = locate_phase15_results()

    print(f"Phase 14 input: {phase14_path}")
    print(f"Phase 15 input: {phase15_path}")

    phase14_df = load_csv_result(
        phase14_path,
        source_phase=14,
    )

    phase15_df = load_csv_result(
        phase15_path,
        source_phase=15,
    )

    classical_rows = convert_to_comparison_rows(
        phase14_df,
        phase=14,
    )

    quantum_rows = convert_to_comparison_rows(
        phase15_df,
        phase=15,
    )

    rows = classical_rows + quantum_rows

    add_model_family(rows)
    validate_rows(rows)

    comparison_df = create_comparison_dataframe(rows)

    metadata = build_metadata(
        phase14_path,
        phase15_path,
        comparison_df,
    )

    save_outputs(
        comparison_df,
        metadata,
    )

    print()
    print("Comparison generated successfully.")
    print()
    print(comparison_df.to_string(index=False))
    print()
    print(f"CSV:      {COMPARISON_CSV}")
    print(f"JSON:     {COMPARISON_JSON}")
    print(f"Metadata: {METADATA_JSON}")
    print()
    print("No models were retrained.")
    print("No test-set tuning was performed.")
    print("Phase 16 comparison artifacts are ready for validation.")


if __name__ == "__main__":
    main()
