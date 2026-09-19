from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_PATH = (
    PROJECT_ROOT
    / "dataset"
    / "dataset_final_phase12.tsv"
)

ARTIFACT_DIR = (
    PROJECT_ROOT
    / "ml"
    / "preprocessing"
    / "artifacts"
)

REPORT_PATH = (
    PROJECT_ROOT
    / "ml"
    / "preprocessing"
    / "PHASE_13_QUALITY_REPORT.md"
)

RANDOM_STATE = 42
TEST_SIZE = 0.20


def main() -> None:
    df = pd.read_csv(
        DATASET_PATH,
        sep="\t",
    )

    X_train = pd.read_csv(
        ARTIFACT_DIR / "X_train.csv"
    )

    X_test = pd.read_csv(
        ARTIFACT_DIR / "X_test.csv"
    )

    y_train = pd.read_csv(
        ARTIFACT_DIR / "y_train.csv"
    )

    y_test = pd.read_csv(
        ARTIFACT_DIR / "y_test.csv"
    )

    feature_metadata = pd.read_csv(
        ARTIFACT_DIR / "feature_metadata.csv"
    )

    label_mapping = pd.read_csv(
        ARTIFACT_DIR / "label_mapping.csv"
    )

    missing_values = df.isna().sum()

    exact_duplicates = int(
        df.duplicated().sum()
    )

    duplicate_frames = int(
        df["frame_number"]
        .duplicated()
        .sum()
    )

    label_counts = (
        df["label"]
        .value_counts()
        .to_dict()
    )

    train_label_counts = (
        y_train["label"]
        .value_counts()
        .sort_index()
        .to_dict()
    )

    test_label_counts = (
        y_test["label"]
        .value_counts()
        .sort_index()
        .to_dict()
    )

    report = f"""# EAG Phase 13 — Dataset Preprocessing Quality Report

## 1. Report Information

- Project: Extension AI Guard (EAG)
- Phase: 13 — Dataset Preprocessing
- Source dataset: `dataset/dataset_final_phase12.tsv`
- Random state: `{RANDOM_STATE}`
- Test size: `{TEST_SIZE}`
- Generated automatically from the verified Phase 13 artifacts.

---

## 2. Original Dataset

| Property | Value |
|---|---:|
| Rows | {df.shape[0]} |
| Columns | {df.shape[1]} |
| Total samples | {len(df)} |
| BENIGN | {label_counts.get("BENIGN", 0)} |
| MALICIOUS | {label_counts.get("MALICIOUS", 0)} |

The frozen Phase 12 dataset contains 144 packet-level samples.

---

## 3. Missing-Value Analysis

| Column | Missing values |
|---|---:|
| `frame_number` | {missing_values["frame_number"]} |
| `time_relative` | {missing_values["time_relative"]} |
| `ip_src` | {missing_values["ip_src"]} |
| `ip_dst` | {missing_values["ip_dst"]} |
| `tcp_srcport` | {missing_values["tcp_srcport"]} |
| `tcp_dstport` | {missing_values["tcp_dstport"]} |
| `frame_len` | {missing_values["frame_len"]} |
| `protocol` | {missing_values["protocol"]} |
| `http_method` | {missing_values["http_method"]} |
| `http_uri` | {missing_values["http_uri"]} |
| `label` | {missing_values["label"]} |

The missing `http_method` and `http_uri` values are structural because most captured packets do not contain HTTP metadata.

`http_method` missing values were converted to the explicit category `MISSING`.

---

## 4. Data Integrity

- Exact duplicate rows: **{exact_duplicates}**
- Duplicate frame-number occurrences: **{duplicate_frames}**
- Duplicate frame numbers were not treated as duplicate packets because frame numbers restart between captures.
- Negative `time_relative` values: **{int((df["time_relative"] < 0).sum())}**
- Non-positive `frame_len` values: **{int((df["frame_len"] <= 0).sum())}**

The packet-size value `10169` was retained because it is a valid observed packet size and was not manually clipped or removed.

---

## 5. Feature Selection

### Retained features

| Feature | Type | Transformation | Reason |
|---|---|---|---|
"""

    for _, row in feature_metadata.iterrows():
        report += (
            f'| `{row["raw_feature"]}` | '
            f'{row["feature_type"]} | '
            f'{row["transformation"]} | '
            f'{row["reason"]} |\n'
        )

    report += """
### Excluded features

| Feature | Decision | Reason |
|---|---|---|
| `http_uri` | Excluded | Controlled endpoint leakage |
| `ip_src` | Excluded | Lab-specific identity |
| `ip_dst` | Excluded | Lab-specific identity |
| `frame_number` | Excluded | Capture-local identifier |
| `tcp_srcport` | Excluded from final feature matrix | Raw lab/capture-specific port identity |
| `tcp_dstport` | Excluded from final feature matrix | Raw lab/capture-specific port identity |

The original fields remain in the Phase 12 dataset for audit and debugging purposes.

---

## 6. Leakage Analysis

The controlled malicious endpoint `/malicious-test` appeared only in MALICIOUS samples, while `/safe` appeared only in BENIGN samples.

Therefore, raw `http_uri` was excluded from the ML feature matrix.

Raw IP addresses were also excluded because they identify the controlled laboratory environment rather than generalized extension behavior.

Raw frame numbers were excluded because they are capture-local identifiers.

Raw port numbers were not used directly as ML categorical features because their values are strongly tied to the controlled capture environment.

These decisions are intended to reduce memorization of the laboratory setup and improve the possibility of generalization to unseen browser extensions.

---

## 7. Label Encoding

"""

    for _, row in label_mapping.iterrows():
        report += (
            f'- `{row["label_name"]}` → '
            f'`{row["label_value"]}`\n'
        )

    report += f"""
---

## 8. Train/Test Split

The dataset was divided using a stratified split with:

- Test size: `{TEST_SIZE}`
- Random state: `{RANDOM_STATE}`
- Stratification target: `label`

### Training set

- Samples: **{len(X_train)}**
- BENIGN: **{(y_train["label"] == 0).sum()}**
- MALICIOUS: **{(y_train["label"] == 1).sum()}**

### Testing set

- Samples: **{len(X_test)}**
- BENIGN: **{(y_test["label"] == 0).sum()}**
- MALICIOUS: **{(y_test["label"] == 1).sum()}**

---

## 9. Numerical Processing

The numerical features are:

- `time_relative`
- `frame_len`

`StandardScaler` was fitted using the training data only.

The fitted scaler was then used to transform both the training and testing sets.

This prevents test-set information from influencing the scaling parameters.

---

## 10. Categorical Processing

The categorical features are:

- `protocol`
- `http_method`

One-hot encoding is used instead of ordinal encoding.

`http_method` missing values are represented explicitly as:

- `MISSING`
- `GET`
- `POST`

Unknown categories during future inference are ignored by the fitted encoder.

---

## 11. Final ML Representation

### Processed training data

- Samples: **{X_train.shape[0]}**
- Features: **{X_train.shape[1]}**

### Processed testing data

- Samples: **{X_test.shape[0]}**
- Features: **{X_test.shape[1]}**

The final preprocessing representation contains **8 ML features**.

---

## 12. Generated Artifacts

The following artifacts were generated:

- `X_train.csv`
- `X_test.csv`
- `y_train.csv`
- `y_test.csv`
- `preprocessor.joblib`
- `label_mapping.csv`
- `feature_metadata.csv`

All artifacts are stored under:

`ml/preprocessing/artifacts/`

---

## 13. Automated Test Results

Phase 13.14 automated validation completed successfully:

**11/11 tests passed.**

The tests verified:

1. Source dataset integrity
2. Label encoding
3. Feature selection
4. Feature types
5. Train/test dimensions
6. Artifact labels
7. Missing processed values
8. Preprocessor artifact
9. Feature metadata
10. Leakage protection
11. Numerical scaling

---

## 14. Reproducibility

The preprocessing process uses:

- Python virtual environment
- pandas
- NumPy
- scikit-learn
- joblib
- Random state: `42`
- Stratified 80/20 train/test split

The fitted preprocessing object is stored as:

`ml/preprocessing/artifacts/preprocessor.joblib`

This allows the same transformations to be reused during later ML training and inference.

---

## 15. Phase 13.15 Status

**QUALITY REPORT GENERATED SUCCESSFULLY**

Phase 13 preprocessing has produced a validated, leakage-aware, reproducible ML-ready dataset.
"""

    REPORT_PATH.write_text(
        report,
        encoding="utf-8",
    )

    print("=" * 60)
    print("EAG PHASE 13 QUALITY REPORT")
    print("=" * 60)
    print(f"Report: {REPORT_PATH}")
    print(f"Original samples: {len(df)}")
    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")
    print(f"Processed features: {X_train.shape[1]}")
    print("Automated tests: 11/11 previously passed")
    print("=" * 60)
    print("QUALITY REPORT GENERATED SUCCESSFULLY")


if __name__ == "__main__":
    main()