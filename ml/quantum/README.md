# Extension AI Guard — Quantum ML Research Lab

## Purpose

This directory contains the quantum machine learning experiments for Extension AI Guard (EAG) Phase 15.

The objective of Phase 15 is to investigate quantum machine learning methods on the same processed dataset used by the Phase 14 classical machine learning experiments.

Phase 15 is a research and experimentation phase. It does not select the final production model.

## Phase 15 Research Question

> Can quantum machine learning models provide a useful and reproducible classification approach for the Extension AI Guard dataset when evaluated under the same data split and feature contract used by the classical machine learning baseline?

The experiment focuses on:

- Reproducibility
- Fair comparison
- Classification performance
- Computational cost
- Circuit/resource characteristics
- Trainability
- Dataset limitations

No quantum advantage is assumed.

## Input Dataset

Quantum experiments use the Phase 13 processed dataset.

The Phase 13 preprocessing contract is fixed and must not be modified for Phase 15.

### Dataset Split

The same stratified split used in Phase 14 is required:

| Dataset | Samples | BENIGN | MALICIOUS |
|---|---:|---:|---:|
| Training | 115 | 89 | 26 |
| Test | 29 | 23 | 6 |

Random state:

```text
42
Feature Count

The processed dataset contains:

8 features

The quantum experiments therefore begin with an 8-qubit candidate configuration.

Quantum ML Approaches

Phase 15 evaluates two primary quantum approaches.

1. Quantum Kernel + QSVC

The first experiment uses a quantum feature map to encode the classical features into a quantum circuit.

A quantum kernel is then constructed from the encoded states.

The resulting kernel is supplied to a Quantum Support Vector Classifier (QSVC).

Conceptually:

Phase 13 features
        |
        v
Quantum Feature Map
        |
        v
Quantum Kernel
        |
        v
QSVC
        |
        v
BENIGN / MALICIOUS

The quantum kernel experiment is the primary Phase 15 quantum classification experiment.

2. Variational Quantum Classifier

The second experiment evaluates a variational quantum classifier.

Conceptually:

Phase 13 features
        |
        v
Feature Encoding
        |
        v
Parameterized Quantum Circuit
        |
        v
Classical Optimizer
        |
        v
VQC Prediction
        |
        v
BENIGN / MALICIOUS

The VQC experiment records optimization and trainability information in addition to classification metrics.

Classical Control

A classical RBF-kernel SVM is used as the matched classical control for the quantum kernel experiment.

This provides a more meaningful comparison than comparing the quantum model against an unrelated algorithm.

The Phase 14 results remain the broader classical baseline.

Phase 15 does not modify or unnecessarily retrain the Phase 14 baseline.

Simulator-First Strategy

Phase 15 begins with quantum simulation.

The initial experiments do not require access to real quantum hardware.

Advantages of the simulator-first approach include:

Deterministic experiment setup
Reproducibility
Easier debugging
Controlled circuit inspection
Lower experimental cost
No dependence on cloud quantum hardware availability

Real quantum hardware is optional and must not be required for Phase 15 completion.

Feature Encoding

The initial candidate encoding strategy is angle encoding.

The eight processed features are mapped into an eight-qubit quantum circuit.

The feature-map design must remain shallow enough to make simulation practical.

Entanglement should be used conservatively.

The experiment should record:

Number of qubits
Feature-map type
Number of repetitions/layers
Entanglement structure
Circuit depth
Circuit size
Simulator configuration
Qubit Strategy

Initial configuration:

Features: 8
Candidate qubits: 8

This provides a direct one-feature-to-one-qubit starting point.

Alternative dimensionality-reduction strategies are outside the initial experiment and should only be introduced if the baseline experiment becomes impractical or a documented research reason requires them.

Quantum Kernel Experiment

The quantum kernel experiment must record:

Feature-map configuration
Qubit count
Circuit depth
Kernel matrix dimensions
Kernel matrix validity
Kernel symmetry
Diagonal behavior
Training time
Inference time
Classification metrics
Random-state configuration where applicable
Kernel Integrity

The generated kernel matrix should be checked for:

Expected dimensions
Finite values
Numerical symmetry within tolerance
Valid diagonal behavior
Absence of unexpected NaN or infinite values
VQC Experiment

The VQC experiment must record:

Feature-map configuration
Ansatz configuration
Number of qubits
Circuit depth
Number of trainable parameters
Optimizer
Optimizer configuration
Maximum iterations/evaluations
Training loss history where available
Convergence information
Training time
Inference time
Classification metrics
Trainability Awareness

Quantum variational models can encounter optimization difficulties.

Phase 15 therefore records trainability-related observations without making unsupported claims.

The experiment should monitor:

Convergence behavior
Loss progression
Optimization stability
Parameter count
Circuit depth
Number of repetitions
Optimization runtime

Potential issues such as barren plateaus are treated as a research consideration rather than an assumed diagnosis.

A failed or poorly converging VQC is still a valid experimental result if the experiment is reproducible and documented correctly.

Evaluation Metrics

Quantum models must be evaluated using the same test set used by the classical experiments.

Required classification metrics:

Accuracy
Precision
Recall
F1-score
ROC-AUC where probability/score output permits
False Positives
False Negatives

Operational measurements should include:

Training time
Inference time
Resource characteristics

The small test set must be explicitly considered when interpreting the results.

Reproducibility

Every experiment should record sufficient configuration information to reproduce the result.

The metadata should include, where applicable:

Python version
Qiskit version
Qiskit Machine Learning version
NumPy version
scikit-learn version
Dataset identifier
Dataset hash
Random seed
Feature count
Qubit count
Feature-map configuration
Ansatz configuration
Optimizer configuration
Simulator configuration
Training configuration
Security and Leakage Controls

The same leakage controls established during Phase 13 remain mandatory.

The quantum models must not use:

Raw source IP addresses
Raw destination IP addresses
Raw HTTP URIs
Raw frame numbers
Capture-specific identifiers
Information derived from the test labels

The Phase 13 preprocessing artifacts remain the source of truth.

Quantum preprocessing must not introduce a second incompatible feature contract.

Dataset Limitations

The Phase 12 dataset is intentionally small and controlled.

It contains:

144 total samples
112 BENIGN
32 MALICIOUS

The Phase 13 test set contains only:

29 samples
23 BENIGN
6 MALICIOUS

Therefore, quantum model results must not be interpreted as proof of real-world generalization or production superiority.

Additional limitations include:

Controlled laboratory traffic
Limited malicious behavior diversity
Small sample size
Limited feature space
Potential simulator/runtime constraints

These limitations must remain visible in Phase 15 results and documentation.

No Quantum Advantage Claim

Phase 15 does not attempt to prove quantum advantage.

A quantum model performing better on this dataset does not establish quantum advantage.

Likewise, a quantum model performing worse does not invalidate quantum machine learning generally.

The experiment is intended to establish a reproducible baseline and generate evidence for the Phase 16 comparison.

Real Quantum Hardware

Real quantum hardware is optional.

If hardware experimentation is performed, the experiment must separately record:

Backend
Hardware configuration
Execution settings
Circuit transpilation information
Shot count
Execution time
Hardware-specific noise considerations

Hardware results must not be mixed with simulator results without clearly identifying the execution environment.

Directory Structure
ml/
└── quantum/
    ├── README.md
    ├── quantum_config.py
    ├── feature_maps.py
    ├── quantum_kernel.py
    ├── train_qsvc.py
    ├── train_vqc.py
    ├── evaluate_quantum_models.py
    ├── benchmark_quantum_models.py
    ├── generate_quantum_metrics.py
    ├── test_quantum_ml.py
    ├── artifacts/
    │   ├── quantum_kernel/
    │   └── vqc/
    └── results/
        ├── quantum_ml_evaluation.csv
        ├── quantum_ml_metrics.json
        └── experiment_metadata.json
Phase 15 Experimental Sequence

The implementation follows this order:

Verify Qiskit environment
Create quantum configuration
Load Phase 13 artifacts
Implement feature-map configuration
Implement quantum kernel experiment
Validate kernel integrity
Train QSVC
Evaluate QSVC
Implement VQC
Train VQC
Record VQC convergence information
Evaluate VQC
Generate quantum metrics
Generate experiment metadata
Run Phase 15 tests
Document results
Commit and push Phase 15
Phase 16 Handoff

Phase 16 will compare:

Phase 14 classical models
Classical RBF SVM control
Quantum Kernel + QSVC
VQC