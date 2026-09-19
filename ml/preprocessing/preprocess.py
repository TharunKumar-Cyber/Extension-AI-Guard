from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler


# ============================================================
# PROJECT CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_PATH = (
    PROJECT_ROOT
    / "dataset"
    / "dataset_final_phase12.tsv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "ml"
    / "preprocessing"
    / "artifacts"
)

RANDOM_STATE = 42
TEST_SIZE = 0.20


# ============================================================
# EXPECTED DATASET SCHEMA
# ============================================================

EXPECTED_COLUMNS = [
    "frame_number",
    "time_relative",
    "ip_src",
    "ip_dst",
    "tcp_srcport",
    "tcp_dstport",
    "frame_len",
    "protocol",
    "http_method",
    "http_uri",
    "label",
]

EXPECTED_LABELS = {
    "BENIGN",
    "MALICIOUS",
}

EXPECTED_PROTOCOLS = {
    "TCP",
    "HTTP",
    "HTTP/JSON",
}

EXPECTED_HTTP_METHODS = {
    "GET",
    "POST",
}


# ============================================================
# FINAL ML FEATURES
# ============================================================

# Features intentionally selected after Phase 13 leakage analysis.
#
# Excluded:
# - frame_number  -> capture-local identifier
# - ip_src        -> lab-specific identity
# - ip_dst        -> lab-specific identity
# - tcp_srcport   -> raw lab/capture-specific port
# - tcp_dstport   -> raw lab/capture-specific port
# - http_uri      -> controlled endpoint leakage
#
# Retained:
# - time_relative -> packet timing behavior
# - frame_len     -> packet size behavior
# - protocol      -> network protocol category
# - http_method   -> HTTP behavior category

NUMERIC_FEATURES = [
    "time_relative",
    "frame_len",
]

CATEGORICAL_FEATURES = [
    "protocol",
    "http_method",
]

FEATURE_COLUMNS = NUMERIC_FEATURES + CATEGORICAL_FEATURES


# ============================================================
# DATASET LOADING AND VALIDATION
# ============================================================

def load_dataset() -> pd.DataFrame:
    """Load and validate the frozen Phase 12 dataset."""

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Phase 12 dataset not found: {DATASET_PATH}"
        )

    df = pd.read_csv(
        DATASET_PATH,
        sep="\t",
    )

    if df.columns.tolist() != EXPECTED_COLUMNS:
        raise ValueError(
            "Dataset schema does not match the expected Phase 12 schema.\n"
            f"Expected: {EXPECTED_COLUMNS}\n"
            f"Actual: {df.columns.tolist()}"
        )

    if df.shape != (144, 11):
        raise ValueError(
            f"Unexpected dataset shape: {df.shape}. "
            "Expected (144, 11)."
        )

    actual_labels = set(
        df["label"].dropna().unique()
    )

    if actual_labels != EXPECTED_LABELS:
        raise ValueError(
            f"Unexpected labels: {actual_labels}. "
            f"Expected: {EXPECTED_LABELS}"
        )

    return df


# ============================================================
# DATA QUALITY VALIDATION
# ============================================================

def validate_data_quality(df: pd.DataFrame) -> None:
    """Validate values required by the preprocessing pipeline."""

    # Numerical columns must be numeric.
    for column in NUMERIC_FEATURES:
        if not pd.api.types.is_numeric_dtype(df[column]):
            raise TypeError(
                f"{column} must contain numeric values."
            )

    # No negative packet lengths.
    if (df["frame_len"] <= 0).any():
        raise ValueError(
            "Invalid frame_len value detected."
        )

    # Relative timestamps may legitimately start at zero,
    # but negative timestamps are invalid.
    if (df["time_relative"] < 0).any():
        raise ValueError(
            "Negative time_relative value detected."
        )

    # Validate protocol categories.
    actual_protocols = set(
        df["protocol"].dropna().unique()
    )

    unexpected_protocols = (
        actual_protocols - EXPECTED_PROTOCOLS
    )

    if unexpected_protocols:
        raise ValueError(
            f"Unexpected protocol values: "
            f"{unexpected_protocols}"
        )

    # HTTP method missing values are legitimate.
    # Convert missing values to an explicit category.
    df["http_method"] = (
        df["http_method"]
        .fillna("MISSING")
        .astype(str)
        .str.strip()
    )

    actual_methods = set(
        df["http_method"].unique()
    )

    allowed_methods = EXPECTED_HTTP_METHODS | {"MISSING"}

    unexpected_methods = (
        actual_methods - allowed_methods
    )

    if unexpected_methods:
        raise ValueError(
            f"Unexpected HTTP method values: "
            f"{unexpected_methods}"
        )

    # No missing values are allowed in final ML features
    # after the explicit HTTP-method conversion.
    missing_features = (
        df[FEATURE_COLUMNS]
        .isna()
        .sum()
    )

    if missing_features.any():
        raise ValueError(
            "Missing values remain in ML features:\n"
            f"{missing_features[missing_features > 0]}"
        )


# ============================================================
# LABEL ENCODING
# ============================================================

def encode_labels(labels: pd.Series) -> pd.Series:
    """Convert BENIGN/MALICIOUS labels to 0/1."""

    label_mapping = {
        "BENIGN": 0,
        "MALICIOUS": 1,
    }

    encoded = labels.map(label_mapping)

    if encoded.isna().any():
        raise ValueError(
            "Unknown label encountered during encoding."
        )

    return encoded.astype("int64")


# ============================================================
# PREPROCESSING PIPELINE
# ============================================================

def build_preprocessor() -> ColumnTransformer:
    """Create the reproducible numerical/categorical preprocessing pipeline."""

    numeric_transformer = StandardScaler()

    categorical_transformer = OneHotEncoder(
        handle_unknown="ignore",
        sparse_output=False,
    )

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "numeric",
                numeric_transformer,
                NUMERIC_FEATURES,
            ),
            (
                "categorical",
                categorical_transformer,
                CATEGORICAL_FEATURES,
            ),
        ],
        remainder="drop",
    )

    return preprocessor


# ============================================================
# ARTIFACT OUTPUT
# ============================================================

def save_artifacts(
    X_train,
    X_test,
    y_train,
    y_test,
    preprocessor,
) -> None:
    """Save ML-ready datasets and preprocessing metadata."""

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # ML-ready feature matrices.
    pd.DataFrame(X_train).to_csv(
        OUTPUT_DIR / "X_train.csv",
        index=False,
    )

    pd.DataFrame(X_test).to_csv(
        OUTPUT_DIR / "X_test.csv",
        index=False,
    )

    # Encoded labels.
    pd.DataFrame(
        {"label": y_train}
    ).to_csv(
        OUTPUT_DIR / "y_train.csv",
        index=False,
    )

    pd.DataFrame(
        {"label": y_test}
    ).to_csv(
        OUTPUT_DIR / "y_test.csv",
        index=False,
    )

    # Reusable fitted preprocessing object.
    joblib.dump(
        preprocessor,
        OUTPUT_DIR / "preprocessor.joblib",
    )

    # Label mapping.
    label_mapping = pd.DataFrame(
        {
            "label_name": [
                "BENIGN",
                "MALICIOUS",
            ],
            "label_value": [
                0,
                1,
            ],
        }
    )

    label_mapping.to_csv(
        OUTPUT_DIR / "label_mapping.csv",
        index=False,
    )

    # Feature metadata.
    feature_metadata = pd.DataFrame(
        {
            "raw_feature": [
                "time_relative",
                "frame_len",
                "protocol",
                "http_method",
            ],
            "feature_type": [
                "numeric",
                "numeric",
                "categorical",
                "categorical",
            ],
            "transformation": [
                "StandardScaler",
                "StandardScaler",
                "OneHotEncoder",
                "OneHotEncoder",
            ],
            "reason": [
                "Packet timing behavior",
                "Packet size behavior",
                "Network protocol category",
                "HTTP behavior category",
            ],
        }
    )

    feature_metadata.to_csv(
        OUTPUT_DIR / "feature_metadata.csv",
        index=False,
    )


# ============================================================
# MAIN PREPROCESSING WORKFLOW
# ============================================================

def main() -> None:
    """Execute the complete Phase 13 preprocessing workflow."""

    print("=" * 60)
    print("EXTENSION AI GUARD - PHASE 13 PREPROCESSING")
    print("=" * 60)

    # --------------------------------------------------------
    # 1. Load dataset
    # --------------------------------------------------------

    print("\n[1/7] Loading Phase 12 dataset...")

    df = load_dataset()

    print(f"Dataset shape: {df.shape}")

    # --------------------------------------------------------
    # 2. Prepare categorical missing values
    # --------------------------------------------------------

    print("\n[2/7] Preparing categorical values...")

    df["http_method"] = (
        df["http_method"]
        .fillna("MISSING")
        .astype(str)
        .str.strip()
    )

    # --------------------------------------------------------
    # 3. Validate data
    # --------------------------------------------------------

    print("\n[3/7] Validating dataset...")

    validate_data_quality(df)

    print("Dataset validation: PASS")

    # --------------------------------------------------------
    # 4. Prepare features and labels
    # --------------------------------------------------------

    print("\n[4/7] Preparing features and labels...")

    X = df[FEATURE_COLUMNS].copy()
    y = encode_labels(df["label"])

    print(f"Raw ML feature columns: {FEATURE_COLUMNS}")
    print(f"Feature rows: {len(X)}")
    print(f"Label distribution:")
    print(
        y.value_counts()
        .sort_index()
        .rename(
            index={
                0: "BENIGN",
                1: "MALICIOUS",
            }
        )
        .to_string()
    )

    # --------------------------------------------------------
    # 5. Stratified train/test split
    # --------------------------------------------------------

    print("\n[5/7] Creating stratified train/test split...")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        stratify=y,
        random_state=RANDOM_STATE,
    )

    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples:  {len(X_test)}")

    # --------------------------------------------------------
    # 6. Fit preprocessing ONLY on training data
    # --------------------------------------------------------

    print("\n[6/7] Fitting preprocessing on training data...")

    preprocessor = build_preprocessor()

    X_train_processed = preprocessor.fit_transform(
        X_train
    )

    X_test_processed = preprocessor.transform(
        X_test
    )

    print(
        "Preprocessing fitted using training data only."
    )

    print(
        f"Processed training shape: "
        f"{X_train_processed.shape}"
    )

    print(
        f"Processed testing shape:  "
        f"{X_test_processed.shape}"
    )

    # --------------------------------------------------------
    # 7. Save ML-ready artifacts
    # --------------------------------------------------------

    print("\n[7/7] Saving preprocessing artifacts...")

    save_artifacts(
        X_train_processed,
        X_test_processed,
        y_train.to_numpy(),
        y_test.to_numpy(),
        preprocessor,
    )

    print(f"Artifacts saved to: {OUTPUT_DIR}")

    print("\n" + "=" * 60)
    print("PHASE 13.12 PREPROCESSING PIPELINE: SUCCESS")
    print("=" * 60)


if __name__ == "__main__":
    main()