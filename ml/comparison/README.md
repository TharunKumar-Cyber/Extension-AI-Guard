**# Extension AI Guard — Phase 16 Model Comparison**



**## Overview**



**Phase 16 performs the formal comparison between the classical machine-learning experiments from Phase 14 and the quantum machine-learning experiments from Phase 15.**



**The comparison consumes previously generated evaluation artifacts.**



**It does \*\*not\*\* retrain models.**



**It does \*\*not\*\* tune models against the test set.**



**The purpose is to provide a reproducible comparison of predictive metrics, computational characteristics, and quantum-specific resource measurements.**



**---**



**## Phase 16 Scope**



**Phase 16 compares:**



**### Classical Models**



**\* Logistic Regression**

**\* Decision Tree**

**\* Random Forest**

**\* SVM**

**\* KNN**

**\* Gradient Boosting**



**### Quantum Models**



**\* Quantum Support Vector Classifier (QSVC)**

**\* Variational Quantum Classifier (VQC)**



**---**



**## Input Artifacts**



**Phase 16 consumes:**



**```text**

**ml/models/classical\_ml\_evaluation.csv**

**```**



**and:**



**```text**

**ml/quantum/results/quantum\_ml\_evaluation.csv**

**```**



**These artifacts were generated during Phases 14 and 15.**



**Phase 16 does not regenerate their model predictions.**



**---**



**## Phase 13 Contract**



**All compared experiments use the established Phase 13 contract:**



**```text**

**Training samples: 115**

**Testing samples: 29**



**Training labels:**

**BENIGN    = 89**

**MALICIOUS = 26**



**Testing labels:**

**BENIGN    = 23**

**MALICIOUS = 6**



**Processed features: 8**

**Random state: 42**

**```**



**The comparison therefore preserves the same dataset and train/test experiment boundary.**



**---**



**## Comparison Metrics**



**Predictive metrics include:**



**\* Accuracy**

**\* Precision**

**\* Recall**

**\* F1-score**

**\* ROC-AUC**

**\* False positives**

**\* False negatives**



**Computational characteristics include:**



**\* Training time**

**\* Inference time**

**\* Inference time per sample**



**Quantum-specific characteristics include:**



**\* Qubit count**

**\* Circuit depth**

**\* Parameter count**

**\* Feature-map configuration**

**\* Ansatz configuration**

**\* Kernel construction characteristics**

**\* Simulator/backend information**

**\* VQC optimization behavior**



**---**



**## Generated Artifacts**



**### Machine-readable comparison**



**```text**

**results/model\_comparison.csv**

**```**



**Contains the normalized comparison table.**



**### Structured comparison**



**```text**

**results/model\_comparison.json**

**```**



**Contains the comparison results in JSON format.**



**### Experiment metadata**



**```text**

**results/comparison\_metadata.json**

**```**



**Records:**



**\* Phase**

**\* Experiment identifier**

**\* Random state**

**\* Dataset contract**

**\* Retraining status**

**\* Test-set tuning status**

**\* Limitations**



**### Human-readable report**



**```text**

**reports/PHASE\_16\_COMPARISON\_REPORT.md**

**```**



**Contains the detailed interpretation of the measured results.**



**---**



**## Scripts**



**### `compare\_models.py`**



**Reads the Phase 14 and Phase 15 evaluation artifacts and produces the normalized Phase 16 comparison outputs.**



**The script does not retrain any model.**



**Run:**



**```text**

**python ml/comparison/compare\_models.py**

**```**



**### `test\_phase16.py`**



**Runs the Phase 16 validation suite using Python's standard-library `unittest` framework.**



**Run:**



**```text**

**python -m unittest ml/comparison/test\_phase16.py -v**

**```**



**---**



**## Testing**



**The Phase 16 validation suite verifies:**



**\* Required comparison directories**

**\* Comparison CSV**

**\* Comparison JSON**

**\* Metadata**

**\* Required columns**

**\* Expected model count**

**\* Phase mapping**

**\* Finite metric values**

**\* Valid false-positive and false-negative counts**

**\* Unique model names**

**\* JSON/CSV consistency**

**\* Metadata contract**

**\* No unsupported quantum-advantage claim**

**\* Preservation of measured Phase 14 and Phase 15 results**



**The current validation result is:**



**```text**

**14 tests**

**14 passed**

**0 failed**

**```**



**---**



**## Important Experimental Rules**



**Phase 16 must not:**



**\* retrain Phase 14 models;**

**\* retrain Phase 15 models;**

**\* modify the Phase 13 dataset;**

**\* modify the Phase 13 train/test split;**

**\* tune models using the test set;**

**\* alter measured results;**

**\* remove models because their results are unfavorable;**

**\* claim quantum advantage without appropriate evidence.**



**---**



**## Dataset Limitation**



**The underlying dataset contains only:**



**```text**

**144 samples**

**```**



**with:**



**```text**

**115 training samples**

**29 testing samples**

**```**



**The test set contains only six MALICIOUS samples.**



**Therefore, small changes in individual predictions can substantially affect reported metrics.**



**Phase 16 results should be interpreted as controlled research measurements rather than evidence of production-level generalization.**



**---**



**## Quantum Experiment Limitation**



**The Phase 15 quantum experiments were performed using a simulator-first configuration.**



**Measured simulator execution time should not be interpreted as a universal measurement of quantum hardware performance.**



**Likewise, these experiments do not establish quantum advantage or quantum supremacy.**



**---**



**## Phase 17 Handoff**



**Phase 16 provides:**



**```text**

**Phase 14 Classical Results**

&#x20;       **+**

**Phase 15 Quantum Results**

&#x20;       **+**

**Phase 16 Formal Comparison**

&#x20;       **↓**

**Phase 17 Model Evaluation**

**```**



**Phase 17 will perform the next level of evaluation while preserving the established Phase 13 experimental contract.**



**---**



**## Directory Structure**



**```text**

**ml/**

**└── comparison/**

&#x20;   **├── README.md**

&#x20;   **├── compare\_models.py**

&#x20;   **├── test\_phase16.py**

&#x20;   **│**

&#x20;   **├── results/**

&#x20;   **│   ├── model\_comparison.csv**

&#x20;   **│   ├── model\_comparison.json**

&#x20;   **│   └── comparison\_metadata.json**

&#x20;   **│**

&#x20;   **└── reports/**

&#x20;       **└── PHASE\_16\_COMPARISON\_REPORT.md**

**```**



**---**



**## Research Position**



**Phase 16 is an evidence-comparison phase.**



**It does not select a final production model.**



**It does not claim that classical or quantum machine learning is universally superior.**



**Its purpose is to preserve the measured experimental evidence and provide a reproducible foundation for Phase 17.**



