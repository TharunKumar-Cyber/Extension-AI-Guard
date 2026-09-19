# Extension AI Guard (EAG)

# Phase 13 — Dataset Preprocessing

## 1. Phase Overview

**Project:** Extension AI Guard (EAG)
**Phase:** 13 — Dataset Preprocessing
**Status:** Complete
**Source Dataset:** `dataset/dataset_final_phase12.tsv`

Phase 13 converts the frozen Phase 12 packet dataset into a validated, leakage-aware, reproducible ML-ready dataset for the later machine-learning phases.

The preprocessing process was designed with one major objective:

> Prepare features that represent network and packet behavior rather than memorizing the controlled laboratory environment.

This is particularly important because the final EAG model is intended to generalize beyond the controlled malicious browser extension used during dataset generation.

---

## 2. Phase 13 Objectives

The objectives of Phase 13 were:

1. Verify the frozen Phase 12 dataset.
2. Validate the dataset schema and labels.
3. Analyze missing values.
4. Check duplicate and data-integrity issues.
5. Identify potential feature leakage.
6. Select appropriate ML features.
7. Prepare numerical features.
8. Prepare categorical features.
9. Transform network-specific information appropriately.
10. Encode the target labels.
11. Create a stratified train/test split.
12. Scale numerical features without test-set leakage.
13. Build a reproducible preprocessing pipeline.
14. Generate ML-ready artifacts.
15. Create automated preprocessing tests.
16. Generate a preprocessing quality report.
17. Document the complete preprocessing methodology.

---

## 3. Phase 13.1 — Environment and Input Verification

The frozen Phase 12 dataset was verified before preprocessing.

### Source dataset

```text
dataset/dataset_final_phase12.tsv
```

Verified properties:

* Rows: **144**
* Columns: **11**
* Data format: **TSV**
* Python environment: project `.venv`
* Python version: **3.13.9**

Required preprocessing libraries were available:

* pandas
* NumPy
* scikit-learn
* joblib

The Phase 12 dataset remained unchanged during preprocessing.

---

## 4. Phase 13.2 — Schema Validation

The dataset was loaded using a tab-separated delimiter.

Expected schema:

```text
frame_number
time_relative
ip_src
ip_dst
tcp_srcport
tcp_dstport
frame_len
protocol
http_method
http_uri
label
```

The verified dataset shape was:

```text
(144, 11)
```

The expected labels were:

```text
BENIGN
MALICIOUS
```

Observed class distribution:

| Label     | Samples |
| --------- | ------: |
| BENIGN    |     112 |
| MALICIOUS |      32 |
| **Total** | **144** |

Schema validation passed successfully.

---

## 5. Phase 13.3 — Missing-Value Analysis

Missing-value analysis produced the following results:

| Column          | Missing |
| --------------- | ------: |
| `frame_number`  |       0 |
| `time_relative` |       0 |
| `ip_src`        |       0 |
| `ip_dst`        |       0 |
| `tcp_srcport`   |       0 |
| `tcp_dstport`   |       0 |
| `frame_len`     |       0 |
| `protocol`      |       0 |
| `http_method`   |     133 |
| `http_uri`      |     122 |
| `label`         |       0 |

The missing HTTP metadata was determined to be structural rather than evidence of corrupted records.

Most captured packets do not contain HTTP-level metadata.

Therefore, rows were not deleted because of missing `http_method` or `http_uri`.

For ML preprocessing, missing `http_method` values were represented explicitly as:

```text
MISSING
```

This prevents the absence of an HTTP method from being confused with a corrupted record.

---

## 6. Phase 13.4 — Duplicate and Data Integrity Analysis

### Exact duplicate rows

```text
0
```

No completely duplicated records were found.

### Duplicate frame numbers

Frame numbers were repeated across the dataset.

The analysis found:

```text
64 unique frame numbers
144 total rows
32 frame numbers appearing more than once
```

This was not treated as a duplicate-record problem.

The reason is that packet frame numbers are local to an individual capture and can restart when a new PCAP capture begins.

Therefore:

```text
frame_number
```

was excluded from the ML feature set because it is a capture-local identifier rather than a general behavioral feature.

### Numerical integrity

The following numerical properties were verified:

* No negative `time_relative` values.
* `time_relative = 0` occurred for legitimate first packets.
* `frame_len` contained valid positive values.
* No invalid negative packet sizes were found.
* Port values were within the observed valid range.

The largest packet size observed was:

```text
10169 bytes
```

This value was retained.

No manual clipping or deletion of the large packet was performed.

---

## 7. Phase 13.5 — Feature Selection and Leakage Analysis

Feature selection was one of the most important parts of Phase 13.

The goal was to avoid allowing the model to memorize the controlled laboratory environment.

### HTTP URI leakage

The following relationship was observed:

| HTTP URI          | BENIGN | MALICIOUS |
| ----------------- | -----: | --------: |
| `/safe`           |     18 |         0 |
| `/malicious-test` |      0 |         4 |
| Missing           |     94 |        28 |

The controlled malicious endpoint was perfectly associated with the MALICIOUS class in the Phase 12 dataset.

If the raw URI were supplied directly to the model, the model could learn:

```text
/malicious-test → MALICIOUS
```

instead of learning general malicious network behavior.

Therefore:

```text
http_uri
```

was excluded from the final ML feature set.

The original URI remains available in the frozen dataset for auditing, debugging, and future explanation purposes.

---

## 8. IP Address Leakage Analysis

The dataset contained two IP addresses:

```text
192.168.31.54
192.168.31.9
```

The class distribution was identical across the observed IP identities.

However, these addresses represent the controlled laboratory environment rather than an intrinsic property of a browser extension.

Therefore:

```text
ip_src
ip_dst
```

were excluded from the ML feature set.

The model should not learn that a particular laboratory machine represents a particular class.

---

## 9. Network Direction Analysis

The observed communication pairs were:

```text
192.168.31.54 → 192.168.31.9
192.168.31.9 → 192.168.31.54
```

Each direction contained:

```text
56 BENIGN
16 MALICIOUS
```

Because the direction did not provide additional class discrimination in this dataset, raw direction was not added as a final ML feature.

This avoids encoding unnecessary laboratory topology information.

---

## 10. Port Analysis

The source and destination port values were examined separately.

Port `9000` appeared in both classes and therefore was not itself a class-exclusive indicator.

However, raw port numbers are strongly related to the controlled test environment and capture roles.

A behavioral port-range transformation was also investigated.

The observed source and destination ports fell into:

```text
REGISTERED
EPHEMERAL
```

with no WELL_KNOWN values in this dataset.

The resulting categories were primarily representative of the capture setup rather than a clear malicious behavioral signal.

Therefore, raw source and destination port values were not included in the final ML feature matrix.

Port analysis remains documented for future feature-engineering consideration.

---

## 11. Final Feature Selection

The final ML feature groups are:

### Numerical features

```text
time_relative
frame_len
```

### Categorical features

```text
protocol
http_method
```

### Excluded raw features

```text
frame_number
ip_src
ip_dst
tcp_srcport
tcp_dstport
http_uri
```

The target variable is:

```text
label
```

---

## 12. Numerical Feature Analysis

### `time_relative`

Observed range:

```text
0.0 → 255.508224
```

The feature represents relative packet timing within the capture.

It was retained because timing behavior can potentially contribute to traffic classification.

It was not a perfect class separator because both classes contained overlapping timing values.

### `frame_len`

Observed range:

```text
54 → 10169
```

The distribution was highly right-skewed.

Common packet sizes included:

```text
54
60
66
89
149
179
211
342
469
10169
```

The large 10169-byte packets were retained because they are valid observations.

The numerical features were standardized later using `StandardScaler`.

---

## 13. Categorical Feature Preparation

### Protocol

Observed protocol categories:

```text
TCP
HTTP
HTTP/JSON
```

The protocol field was retained as a categorical feature.

### HTTP method

Observed values:

```text
GET
POST
MISSING
```

The missing HTTP method was explicitly represented as:

```text
MISSING
```

Categorical features were encoded using one-hot encoding rather than ordinal encoding.

This prevents categories from being assigned artificial numerical ordering.

---

## 14. Phase 13.9 — Label Encoding

The target mapping was defined as:

```text
BENIGN   → 0
MALICIOUS → 1
```

The original class distribution was preserved.

No duplication or deletion of minority-class samples was performed during preprocessing.

---

## 15. Phase 13.10 — Train/Test Split

A stratified train/test split was used.

Configuration:

```text
Test size: 20%
Random state: 42
Stratification: label
```

Result:

### Training set

```text
115 samples
89 BENIGN
26 MALICIOUS
```

### Testing set

```text
29 samples
23 BENIGN
6 MALICIOUS
```

The split was performed before fitting preprocessing transformations.

This is important because preprocessing parameters must not be learned from the test set.

---

## 16. Phase 13.11 — Numerical Scaling

The numerical features:

```text
time_relative
frame_len
```

were standardized using:

```text
StandardScaler
```

The scaler was fitted using the training set only.

The same fitted scaler was then applied to both:

```text
X_train
X_test
```

Verification produced:

```text
Training means after scaling:
approximately [0, 0]

Training standard deviation:
[1, 1]
```

The test set contained:

```text
29 samples
2 numerical input features
```

This confirms that numerical scaling was correctly applied without fitting on test data.

---

## 17. Phase 13.12 — Reproducible Preprocessing Pipeline

The complete preprocessing pipeline performs:

```text
Phase 12 frozen dataset
        ↓
Dataset loading
        ↓
Schema validation
        ↓
Data quality validation
        ↓
HTTP missing-value handling
        ↓
Feature selection
        ↓
Label encoding
        ↓
Stratified train/test split
        ↓
Numerical StandardScaler
        ↓
Categorical OneHotEncoder
        ↓
ML-ready feature matrices
```

The pipeline is implemented in:

```text
ml/preprocessing/preprocess.py
```

The pipeline uses:

```text
random_state = 42
test_size = 0.20
```

Categorical preprocessing uses:

```text
OneHotEncoder(
    handle_unknown="ignore",
    sparse_output=False
)
```

This allows the later inference pipeline to handle previously unseen categorical values without crashing.

---

## 18. Final ML Representation

The final raw feature set contains:

```text
2 numerical features
2 categorical features
```

After preprocessing:

```text
2 numerical features
+
3 protocol categories
+
3 HTTP-method categories
=
8 processed ML features
```

Verified processed dimensions:

```text
Training: (115, 8)
Testing:  (29, 8)
```

Therefore, Phase 13 produces an **8-dimensional ML-ready feature representation**.

---

## 19. Phase 13.13 — Generated Artifacts

The following artifacts were successfully generated:

```text
ml/preprocessing/artifacts/
├── X_train.csv
├── X_test.csv
├── y_train.csv
├── y_test.csv
├── preprocessor.joblib
├── label_mapping.csv
└── feature_metadata.csv
```

### Artifact purposes

| Artifact               | Purpose                                   |
| ---------------------- | ----------------------------------------- |
| `X_train.csv`          | Processed training features               |
| `X_test.csv`           | Processed testing features                |
| `y_train.csv`          | Encoded training labels                   |
| `y_test.csv`           | Encoded testing labels                    |
| `preprocessor.joblib`  | Reusable fitted preprocessing transformer |
| `label_mapping.csv`    | BENIGN/MALICIOUS mapping                  |
| `feature_metadata.csv` | Feature transformation metadata           |

---

## 20. Phase 13.14 — Automated Testing

An automated test suite was created:

```text
ml/preprocessing/test_preprocess.py
```

The test suite verified:

1. Source dataset integrity
2. Label encoding
3. Feature selection
4. Feature types
5. Train/test dimensions
6. Artifact labels
7. Missing processed values
8. Preprocessor artifact loading
9. Feature metadata
10. Leakage protection
11. Numerical scaling

Final result:

```text
ALL TESTS PASSED: 11/11
```

This provides automated protection against accidental preprocessing regressions.

---

## 21. Phase 13.15 — Quality Report

A separate automated quality-report generator was created:

```text
ml/preprocessing/generate_quality_report.py
```

The generated report is:

```text
ml/preprocessing/PHASE_13_QUALITY_REPORT.md
```

The report records:

* Original dataset size
* Class distribution
* Missing-value analysis
* Duplicate analysis
* Data-integrity results
* Feature selection
* Leakage decisions
* Label encoding
* Train/test split
* Numerical scaling
* Categorical encoding
* Final ML dimensions
* Generated artifacts
* Automated test status
* Reproducibility settings

The report was generated successfully from the actual Phase 13 artifacts.

---

## 22. Reproducibility

Phase 13 uses deterministic preprocessing settings.

Important reproducibility parameters:

```text
Random state: 42
Test size: 0.20
Split strategy: Stratified
Numerical scaler: StandardScaler
Categorical encoder: OneHotEncoder
```

The fitted preprocessing object is stored as:

```text
ml/preprocessing/artifacts/preprocessor.joblib
```

This object can later be reused during ML training and real-time inference so that the same transformations are applied consistently.

---

## 23. Leakage Prevention Strategy

Phase 13 explicitly prevents several forms of dataset-specific memorization.

Excluded:

```text
http_uri
ip_src
ip_dst
frame_number
tcp_srcport
tcp_dstport
```

The most significant identified leakage source was:

```text
/malicious-test
```

because it was perfectly associated with the MALICIOUS label in the controlled Phase 12 dataset.

The preprocessing design therefore prioritizes behavioral features over laboratory identifiers.

This is important for the long-term EAG objective of testing arbitrary browser extensions rather than only the controlled malicious extension used during dataset generation.

---

## 24. Current Limitations

The Phase 12 dataset is relatively small:

```text
144 total samples
112 BENIGN
32 MALICIOUS
```

It was generated from a controlled laboratory environment.

Therefore, Phase 13 does not claim that the selected features are already sufficient for production-grade malicious-extension detection.

The later ML phases must evaluate:

* Generalization
* False positives
* False negatives
* Class imbalance effects
* Model robustness
* Unseen traffic behavior
* Performance on additional extension traffic

The current preprocessing pipeline is designed to provide a clean and reproducible foundation for those experiments.

---

## 25. Phase 14 Handoff

Phase 13 provides the following ML-ready inputs for Phase 14:

```text
X_train.csv
X_test.csv
y_train.csv
y_test.csv
preprocessor.joblib
feature_metadata.csv
label_mapping.csv
```

Phase 14 — Classical ML can now use the processed training and testing datasets without repeating the Phase 13 preprocessing logic.

The fitted preprocessing object should also be reused when preparing future inference data.

---

## 26. Phase Completion Criteria

| Requirement                  | Status  |
| ---------------------------- | ------- |
| Dataset verified             | ✅       |
| Schema validated             | ✅       |
| Missing values analyzed      | ✅       |
| Duplicate/integrity analysis | ✅       |
| Leakage analysis             | ✅       |
| Feature selection            | ✅       |
| Numerical preparation        | ✅       |
| Categorical preparation      | ✅       |
| Network/IP analysis          | ✅       |
| Label encoding               | ✅       |
| Stratified train/test split  | ✅       |
| Numerical scaling            | ✅       |
| Reproducible pipeline        | ✅       |
| ML-ready artifacts           | ✅       |
| Automated tests              | ✅ 11/11 |
| Quality report               | ✅       |
| Documentation                | ✅       |

---

# Phase 13 — Completion

**Extension AI Guard Phase 13 — Dataset Preprocessing is complete.**

The frozen Phase 12 dataset has been transformed into a validated, leakage-aware, reproducible ML-ready dataset.

The resulting representation contains:

```text
115 training samples
29 testing samples
8 processed features
BENIGN = 0
MALICIOUS = 1
```

The preprocessing pipeline, artifacts, automated tests, quality report, and documentation are all present in the project.

**Next official roadmap phase:**

> **Phase 14 — Classical Machine Learning**
