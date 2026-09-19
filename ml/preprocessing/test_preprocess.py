from pathlib import Path

import joblib
import pandas as pd

from preprocess import (
    CATEGORICAL_FEATURES,
    DATASET_PATH,
    EXPECTED_COLUMNS,
    FEATURE_COLUMNS,
    NUMERIC_FEATURES,
    OUTPUT_DIR,
    encode_labels,
    load_dataset,
)


# ============================================================
# TEST HELPERS
# ============================================================

def assert_condition(condition: bool, message: str) -> None:
    """Raise an assertion error with a clear message."""

    if not condition:
        raise AssertionError(message)


# ============================================================
# TEST 1 — SOURCE DATASET
# ============================================================

def test_source_dataset() -> None:
    """Verify the frozen Phase 12 dataset exists and is valid."""

    assert_condition(
        DATASET_PATH.exists(),
        f"Dataset does not exist: {DATASET_PATH}",
    )

    df = load_dataset()

    assert_condition(
        df.shape == (144, 11),
        f"Unexpected dataset shape: {df.shape}",
    )

    assert_condition(
        df.columns.tolist() == EXPECTED_COLUMNS,
        "Dataset columns do not match expected schema.",
    )

    print("PASS: Source dataset")


# ============================================================
# TEST 2 — LABEL ENCODING
# ============================================================

def test_label_encoding() -> None:
    """Verify BENIGN/MALICIOUS label encoding."""

    df = load_dataset()

    encoded = encode_labels(df["label"])

    assert_condition(
        set(encoded.unique()) == {0, 1},
        f"Unexpected encoded labels: {set(encoded.unique())}",
    )

    assert_condition(
        encoded.value_counts().to_dict() == {
            0: 112,
            1: 32,
        },
        "Encoded label distribution is incorrect.",
    )

    print("PASS: Label encoding")


# ============================================================
# TEST 3 — FEATURE SELECTION
# ============================================================

def test_feature_selection() -> None:
    """Verify only approved ML features are used."""

    expected_features = [
        "time_relative",
        "frame_len",
        "protocol",
        "http_method",
    ]

    assert_condition(
        FEATURE_COLUMNS == expected_features,
        f"Unexpected feature list: {FEATURE_COLUMNS}",
    )

    forbidden_features = {
        "frame_number",
        "ip_src",
        "ip_dst",
        "tcp_srcport",
        "tcp_dstport",
        "http_uri",
        "label",
    }

    overlap = set(FEATURE_COLUMNS) & forbidden_features

    assert_condition(
        not overlap,
        f"Forbidden/leaky features detected: {overlap}",
    )

    print("PASS: Feature selection")


# ============================================================
# TEST 4 — FEATURE TYPES
# ============================================================

def test_feature_types() -> None:
    """Verify numeric and categorical feature groups."""

    assert_condition(
        NUMERIC_FEATURES == [
            "time_relative",
            "frame_len",
        ],
        "Numeric feature definition is incorrect.",
    )

    assert_condition(
        CATEGORICAL_FEATURES == [
            "protocol",
            "http_method",
        ],
        "Categorical feature definition is incorrect.",
    )

    print("PASS: Feature types")


# ============================================================
# TEST 5 — TRAIN/TEST DIMENSIONS
# ============================================================

def test_train_test_dimensions() -> None:
    """Verify generated train/test artifact dimensions."""

    X_train = pd.read_csv(
        OUTPUT_DIR / "X_train.csv"
    )

    X_test = pd.read_csv(
        OUTPUT_DIR / "X_test.csv"
    )

    y_train = pd.read_csv(
        OUTPUT_DIR / "y_train.csv"
    )

    y_test = pd.read_csv(
        OUTPUT_DIR / "y_test.csv"
    )

    assert_condition(
        X_train.shape == (115, 8),
        f"Unexpected X_train shape: {X_train.shape}",
    )

    assert_condition(
        X_test.shape == (29, 8),
        f"Unexpected X_test shape: {X_test.shape}",
    )

    assert_condition(
        y_train.shape == (115, 1),
        f"Unexpected y_train shape: {y_train.shape}",
    )

    assert_condition(
        y_test.shape == (29, 1),
        f"Unexpected y_test shape: {y_test.shape}",
    )

    assert_condition(
        len(X_train) == len(y_train),
        "Training feature/label counts do not match.",
    )

    assert_condition(
        len(X_test) == len(y_test),
        "Testing feature/label counts do not match.",
    )

    print("PASS: Train/test dimensions")


# ============================================================
# TEST 6 — LABEL VALUES IN ARTIFACTS
# ============================================================

def test_artifact_labels() -> None:
    """Verify ML-ready labels contain only 0 and 1."""

    y_train = pd.read_csv(
        OUTPUT_DIR / "y_train.csv"
    )["label"]

    y_test = pd.read_csv(
        OUTPUT_DIR / "y_test.csv"
    )["label"]

    allowed = {0, 1}

    assert_condition(
        set(y_train.unique()).issubset(allowed),
        "Unexpected value found in y_train.",
    )

    assert_condition(
        set(y_test.unique()).issubset(allowed),
        "Unexpected value found in y_test.",
    )

    print("PASS: Artifact labels")


# ============================================================
# TEST 7 — NO MISSING ML VALUES
# ============================================================

def test_no_missing_values() -> None:
    """Verify processed feature matrices contain no missing values."""

    X_train = pd.read_csv(
        OUTPUT_DIR / "X_train.csv"
    )

    X_test = pd.read_csv(
        OUTPUT_DIR / "X_test.csv"
    )

    assert_condition(
        not X_train.isna().any().any(),
        "Missing values found in X_train.",
    )

    assert_condition(
        not X_test.isna().any().any(),
        "Missing values found in X_test.",
    )

    print("PASS: No missing processed values")


# ============================================================
# TEST 8 — PREPROCESSOR ARTIFACT
# ============================================================

def test_preprocessor_artifact() -> None:
    """Verify the fitted preprocessing object exists and loads."""

    preprocessor_path = (
        OUTPUT_DIR / "preprocessor.joblib"
    )

    assert_condition(
        preprocessor_path.exists(),
        "preprocessor.joblib does not exist.",
    )

    preprocessor = joblib.load(
        preprocessor_path
    )

    assert_condition(
        hasattr(preprocessor, "transform"),
        "Loaded preprocessor has no transform method.",
    )

    print("PASS: Preprocessor artifact")


# ============================================================
# TEST 9 — FEATURE METADATA
# ============================================================

def test_feature_metadata() -> None:
    """Verify feature metadata was generated correctly."""

    metadata_path = (
        OUTPUT_DIR / "feature_metadata.csv"
    )

    assert_condition(
        metadata_path.exists(),
        "feature_metadata.csv does not exist.",
    )

    metadata = pd.read_csv(
        metadata_path
    )

    assert_condition(
        metadata.shape[0] == 4,
        f"Unexpected metadata rows: {metadata.shape[0]}",
    )

    assert_condition(
        set(metadata["raw_feature"])
        == set(FEATURE_COLUMNS),
        "Feature metadata does not match selected features.",
    )

    print("PASS: Feature metadata")


# ============================================================
# TEST 10 — LEAKAGE PROTECTION
# ============================================================

def test_leakage_protection() -> None:
    """Verify known leakage-prone raw fields are absent."""

    X_train = pd.read_csv(
        OUTPUT_DIR / "X_train.csv"
    )

    X_test = pd.read_csv(
        OUTPUT_DIR / "X_test.csv"
    )

    # The processed feature matrix must contain only
    # transformed ML features, not raw identity fields.
    forbidden_names = {
        "frame_number",
        "ip_src",
        "ip_dst",
        "tcp_srcport",
        "tcp_dstport",
        "http_uri",
        "label",
    }

    actual_columns = (
        set(X_train.columns)
        | set(X_test.columns)
    )

    overlap = actual_columns & forbidden_names

    assert_condition(
        not overlap,
        f"Potential leakage fields found: {overlap}",
    )

    print("PASS: Leakage protection")


# ============================================================
# TEST 11 — SCALING CHECK
# ============================================================

def test_scaling() -> None:
    """Verify numerical features were standardized."""

    X_train = pd.read_csv(
        OUTPUT_DIR / "X_train.csv"
    )

    # The first two processed columns correspond to:
    # time_relative and frame_len.
    numeric_data = X_train.iloc[:, :2]

    means = numeric_data.mean().abs()

    stds = numeric_data.std(
        ddof=0
    )

    assert_condition(
        (means < 1e-10).all(),
        f"Training means are not approximately zero: {means.tolist()}",
    )

    assert_condition(
        ((stds - 1).abs() < 1e-10).all(),
        f"Training standard deviations are not approximately one: "
        f"{stds.tolist()}",
    )

    print("PASS: Numerical scaling")


# ============================================================
# RUN ALL TESTS
# ============================================================

def main() -> None:
    """Run all Phase 13 preprocessing tests."""

    print("=" * 60)
    print("EXTENSION AI GUARD - PHASE 13 AUTOMATED TESTS")
    print("=" * 60)

    tests = [
        test_source_dataset,
        test_label_encoding,
        test_feature_selection,
        test_feature_types,
        test_train_test_dimensions,
        test_artifact_labels,
        test_no_missing_values,
        test_preprocessor_artifact,
        test_feature_metadata,
        test_leakage_protection,
        test_scaling,
    ]

    passed = 0

    for test in tests:
        test()
        passed += 1

    print("\n" + "=" * 60)
    print(
        f"ALL TESTS PASSED: {passed}/{len(tests)}"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()