# Phase 15 — Quantum Machine Learning Research Lab

## 1. Phase Overview

Phase 15 introduces a controlled Quantum Machine Learning (QML) research experiment into Extension AI Guard (EAG).

The purpose is to investigate whether quantum machine-learning approaches can learn the same binary network-traffic classification problem represented by the frozen Phase 13 feature space, and to measure their performance, computational characteristics, reproducibility, and limitations against classical baselines.

This phase is a research and experimentation phase. It does not select the final EAG production model.

---

## 2. Relationship to the EAG Roadmap

The Phase 15 workflow is:

```text
Phase 12
Frozen Dataset
     ↓
Phase 13
Dataset Preprocessing
     ↓
Phase 14
Classical ML Baselines
     ↓
Phase 15
Quantum ML Research Lab
     ↓
Phase 16
Classical vs Quantum Comparison
     ↓
Phase 17
Model Evaluation

Phase 15 uses the same processed dataset and train/test split established in Phase 13 so that later comparisons remain controlled.

3. Phase 13 Input Contract

Phase 15 consumes the verified Phase 13 artifacts.

Training set:

115 samples
89 BENIGN
26 MALICIOUS

Testing set:

29 samples
23 BENIGN
6 MALICIOUS

Processed feature count:

8 features

Feature mapping:

time_relative
frame_len
protocol_HTTP
protocol_HTTP_JSON
protocol_TCP
http_method_GET
http_method_POST
http_method_MISSING

Label mapping:

BENIGN = 0
MALICIOUS = 1

Random state:

42

Phase 13 preprocessing artifacts were reused rather than independently recreated.

4. Research Question

The primary research question is:

Can quantum machine-learning methods learn the EAG binary traffic-classification problem represented by the Phase 13 feature space, and how do their observed predictive and computational characteristics compare with established classical baselines?

The experiment distinguishes measured results from theoretical expectations.

5. Research Principles

Phase 15 follows these principles:

Same dataset
Same train/test split
Same labels
Same feature contract
Reproducible configuration
Simulator-first execution
Controlled experiments
Explicit quantum-resource measurements
No test-set tuning
No unsupported quantum-advantage claims
Clear documentation of limitations

The objective is to produce a defensible QML research experiment rather than artificially maximize a score.

6. Selected Quantum ML Approaches

Two QML approaches were investigated.

6.1 Primary: Quantum Kernel + QSVC

The classical feature vector is mapped into a quantum state using a quantum feature map.

Quantum-state similarity is then used to construct a kernel matrix.

The resulting quantum kernel is supplied to a Support Vector Classifier.

Pipeline:

Classical Features
        ↓
Quantum Feature Map
        ↓
Quantum States
        ↓
Quantum Kernel
        ↓
Kernel Matrix
        ↓
QSVC
        ↓
BENIGN / MALICIOUS

The quantum-kernel experiment is the primary QML experiment.

6.2 Secondary: Variational Quantum Classifier

A Variational Quantum Classifier (VQC) provides a second QML approach.

Pipeline:

Classical Features
        ↓
Quantum Feature Map
        ↓
Parameterized Quantum Circuit
        ↓
Measurement
        ↓
Optimization
        ↓
Classification
        ↓
BENIGN / MALICIOUS

The VQC experiment records optimization and trainability information in addition to ordinary classification metrics.

7. Classical Control

The quantum-kernel experiment is intended to be compared with a matched classical RBF SVM control.

The control uses:

Same Phase 13 data
Same train/test split
Same preprocessing
Random state 42 where applicable
No test-set tuning

Formal comparison with the Phase 14 classical results is performed in Phase 16.

8. Quantum Framework

The verified Phase 15 environment uses:

Qiskit 2.5.2
Qiskit Machine Learning 0.9.1
qiskit-algorithms 0.4.0
cloudpickle 3.1.2

The installed versions were verified before implementation.

The implementation uses APIs compatible with the installed Qiskit 2.x environment.

9. Simulator-First Strategy

Phase 15 was executed using a local simulator-first configuration.

Configuration:

Execution mode: simulator-first
Backend: statevector
Shots: None for the quantum-kernel configuration

For the VQC, StatevectorSampler was configured with:

Default shots: 1024
Seed: 42

Reasons for simulator-first execution:

Reproducibility
Deterministic debugging
No cloud dependency
No hardware queue dependency
Easier automated testing
Controlled experimentation

No real quantum hardware execution was required for Phase 15 completion.

10. Feature Encoding Strategy

The initial encoding strategy uses angle-based quantum feature encoding through a Qiskit ZZ feature map.

The eight processed features are represented by eight quantum parameters.

The feature-map configuration is:

Feature-map type: ZZ feature map
Qubits: 8
Repetitions: 1
Entanglement: linear

The implementation uses the installed Qiskit API:

zz_feature_map(...)

The resulting feature map was verified to contain:

Qubits: 8
Parameters: 8
Depth: 23
Size: 37
11. Qubit Strategy

The initial configuration uses:

8 processed features
        ↓
8 qubits

This configuration was retained because it directly represents the eight-dimensional Phase 13 feature space without introducing an additional dimensionality-reduction experiment.

No alternative dimensionality-reduction configuration was silently substituted.

12. Quantum Kernel Experiment

The quantum-kernel experiment performed the following:

Loaded the Phase 13 processed training data.
Loaded the Phase 13 processed test data.
Constructed the quantum feature map.
Constructed a FidelityQuantumKernel.
Generated the training kernel matrix.
Trained QSVC.
Reloaded the saved QSVC artifact independently.
Evaluated QSVC on the untouched Phase 13 test set.
Calculated classification metrics.
Recorded kernel integrity information.
Saved model, kernel, evaluation, and metadata artifacts.
Kernel configuration
Kernel: FidelityQuantumKernel
Qubits: 8
Feature-map repetitions: 1
Entanglement: linear
Kernel matrix

Measured training kernel matrix:

Shape: (115, 115)
Minimum: 0.000000016760
Maximum: 1.000000000004
Mean: 0.258488765979
Diagonal mean: 1.000000000002

Integrity checks confirmed:

Correct dimensions
Finite values
Symmetry
Diagonal values near 1
QSVC training

Measured training time:

28.624561 seconds

The saved model was independently reloaded successfully.

Support-vector information:

Support vectors: [40, 26]
QSVC test evaluation

The untouched Phase 13 test set contained:

29 samples
23 BENIGN
6 MALICIOUS

Measured results:

Metric	QSVC
Accuracy	0.7586
Precision	0.0000
Recall	0.0000
F1-score	0.0000
ROC-AUC	0.7391
True negatives	22
False positives	1
False negatives	6
True positives	0
Total inference time	16.907764 s
Inference time/sample	583.026338 ms

ROC-AUC was calculated from the QSVC decision_function, because the saved QSVC configuration does not expose predict_proba.

The measured result means QSVC correctly classified 22 of 23 benign samples but classified none of the six malicious test samples as malicious at the classifier's decision threshold.

13. VQC Experiment

The VQC experiment was executed using the same Phase 13 train/test contract.

Configuration:

Qubits: 8
Feature-map repetitions: 1
Ansatz: Real Amplitudes
Ansatz repetitions: 1
Ansatz entanglement: linear
Optimizer: COBYLA
Maximum iterations: 100
Tolerance: 0.001
Sampler: StatevectorSampler
Default shots: 1024
Seed: 42
VQC training

Measured training time:

41.913872 seconds

Objective evaluations:

100

Loss history:

Initial loss: 1.228184916450
Final loss: 0.966805365648
Minimum loss: 0.965840828639

The trained VQC artifact was successfully saved and independently reloaded.

VQC test evaluation

Measured results:

Metric	VQC
Accuracy	0.6897
Precision	0.0000
Recall	0.0000
F1-score	0.0000
ROC-AUC	0.3442
True negatives	20
False positives	3
False negatives	6
True positives	0
Total inference time	0.134255 s
Inference time/sample	4.629493 ms

The VQC predicted none of the six malicious test samples correctly at its classification threshold.

The ROC-AUC value was derived from the model's available probability output.

14. Trainability and Barren-Plateau Awareness

Phase 15 records trainability-related observations without claiming the presence or absence of barren plateaus.

Observed VQC information includes:

Circuit configuration
Number of qubits
Ansatz repetitions
Optimizer
Maximum iterations
Objective evaluations
Initial loss
Final loss
Minimum loss
Training time

The loss history was successfully generated and persisted.

The observed loss behavior alone is not sufficient to establish a barren plateau.

Therefore, Phase 15 makes no barren-plateau diagnosis.

15. Metrics

Standard classification metrics generated:

Accuracy
Precision
Recall
F1-score
ROC-AUC
False positives
False negatives
True positives
True negatives

Quantum-specific measurements generated where applicable:

Qubit count
Circuit configuration
Feature-map repetitions
Entanglement configuration
Ansatz configuration
Kernel construction
Kernel matrix dimensions
Kernel integrity
Training time
Inference time
Optimizer configuration
VQC loss history
Simulator information
16. Reproducibility Metadata

Phase 15 records reproducibility metadata including:

EAG phase
Configuration version
Execution mode
Random state
Classical control
Quantum-kernel configuration
Qubit count
Feature-map repetitions
Entanglement
Simulator backend
VQC configuration
Ansatz repetitions
Optimizer
Maximum iterations
Artifact paths
Experiment generation timestamp

Configuration version:

phase15-v1

Random state:

42
17. Implementation Structure

The Phase 15 implementation is:

ml/
└── quantum/
    ├── README.md
    ├── quantum_config.py
    ├── feature_maps.py
    ├── quantum_kernel.py
    ├── train_qsvc.py
    ├── generate_kernel_matrix.py
    ├── train_vqc.py
    ├── evaluate_qsvc.py
    ├── evaluate_vqc.py
    ├── build_quantum_results.py
    ├── test_phase15.py
    │
    ├── artifacts/
    │   ├── quantum_kernel/
    │   │   ├── qsvc_model.joblib
    │   │   └── kernel_matrix.npy
    │   └── vqc/
    │       ├── vqc_model.joblib
    │       └── loss_history.csv
    │
    └── results/
        ├── qsvc_evaluation.csv
        ├── vqc_evaluation.csv
        ├── quantum_ml_evaluation.csv
        ├── quantum_ml_metrics.json
        └── experiment_metadata.json
18. Proposed Experiments
Experiment A — Quantum Kernel + QSVC

Completed.

Measured:

Classification performance
Kernel integrity
Kernel matrix
Training time
Inference time
Model reloadability
Circuit configuration
Experiment B — VQC

Completed.

Measured:

Classification performance
Training convergence
Loss behavior
Circuit configuration
Training time
Inference time
Model reloadability
Experiment C — Classical RBF SVM Control

The classical RBF SVM was established in Phase 14.

Formal comparison with the Phase 15 quantum experiments is reserved for Phase 16.

19. Fair Experimental Comparison

The quantum experiments used:

Phase 13 Dataset
        ↓
Phase 13 Preprocessing
        ↓
Phase 13 Train/Test Split
        ↓
Quantum Models

The test set was not used for model training or repeated test-set tuning.

The same frozen Phase 13 test set was used for both QSVC and VQC evaluation.

No dataset modification was performed to improve QML results.

20. Artifacts

Phase 15 generated the following artifacts.

Quantum model artifacts
ml/quantum/artifacts/quantum_kernel/qsvc_model.joblib
ml/quantum/artifacts/quantum_kernel/kernel_matrix.npy
ml/quantum/artifacts/vqc/vqc_model.joblib
ml/quantum/artifacts/vqc/loss_history.csv
Evaluation artifacts
ml/quantum/results/qsvc_evaluation.csv
ml/quantum/results/vqc_evaluation.csv
ml/quantum/results/quantum_ml_evaluation.csv
Metadata artifacts
ml/quantum/results/quantum_ml_metrics.json
ml/quantum/results/experiment_metadata.json

The artifacts were successfully generated and validated.

21. Testing Requirements

The Phase 15 automated test suite verifies:

Quantum configuration
Feature-map construction
QSVC model reload
VQC model reload
Kernel matrix integrity
VQC loss history
QSVC evaluation artifact
VQC evaluation artifact
Unified evaluation artifact
Metrics JSON
Experiment metadata

Final automated test result:

11/11 tests passed

All Phase 15 tests passed successfully.

22. Security and Leakage Controls

Phase 13 leakage controls remain mandatory.

The following lab-specific identifiers were not reintroduced as model features:

Raw IP addresses
Frame numbers
Raw HTTP URI
Capture-specific port identifiers

The quantum models therefore operate on the controlled eight-feature representation established by Phase 13.

23. Dataset Limitations

The current dataset is intentionally small:

144 total samples
115 training samples
29 testing samples

The test set contains:

23 BENIGN
6 MALICIOUS

The small number of malicious test samples makes the measured metrics sensitive to individual predictions.

For example, both QML models produced:

True positives = 0
False negatives = 6

Therefore, the Phase 15 results must not be interpreted as evidence of real-world generalization.

The controlled laboratory dataset is suitable for demonstrating the research pipeline, not for proving production-level detection performance.

24. No Quantum Advantage Claim

Phase 15 does not claim:

Quantum advantage
Quantum supremacy
Production superiority
Real-world superiority
Guaranteed generalization
Faster classification than classical ML

The observed QSVC and VQC results are experimental measurements under the specific Phase 15 configuration.

Formal comparison against Phase 14 classical models belongs to Phase 16.

25. Real Hardware Policy

Real QPU execution is optional.

Phase 15 was completed using simulator-first execution.

No real quantum hardware result is included in the Phase 15 primary results.

If hardware execution is performed in a future controlled experiment, the following must be recorded:

Hardware backend
Date/time
Number of shots
Circuit configuration
Qubit configuration
Transpilation information where relevant
Execution cost/time
Result differences from simulation

Simulator results remain the primary reproducible Phase 15 baseline.

26. Phase 15 Completion Criteria

Phase 15 status:

 Phase 15 documentation is implemented and updated.
 Qiskit environment is verified.
 Phase 13 input contract is verified.
 Quantum feature encoding is implemented and tested.
 Quantum Kernel + QSVC is implemented.
 VQC is implemented.
 Classical RBF SVM control is available from Phase 14.
 Quantum experiments execute successfully.
 Classification metrics are generated.
 Quantum-specific metrics are generated.
 Experiment metadata is generated.
 Model/artifact files are saved.
 Automated tests pass.
 Results and limitations are documented.
 No unsupported quantum-advantage claim is made.
 Phase 16 handoff is documented.
 Git working tree is clean.
 Phase 15 changes are committed and pushed.

The final two criteria remain unchecked until Git verification, commit, and push are completed.

27. Phase 16 Handoff

Phase 15 provides the following inputs to Phase 16:

Phase 14 Classical ML Results
        +
Phase 15 Quantum ML Results
        ↓
Phase 16 Formal Model Comparison

Phase 15 measured quantum results:

Model	Accuracy	Precision	Recall	F1	ROC-AUC
QSVC	0.7586	0.0000	0.0000	0.0000	0.7391
VQC	0.6897	0.0000	0.0000	0.0000	0.3442

Phase 16 will compare these results with the Phase 14 classical models using the documented experimental evidence.

Phase 15 itself does not select a final production model.

28. Research Conclusion

Phase 15 established a controlled and reproducible Quantum Machine Learning research track for Extension AI Guard.

The experiment successfully implemented and evaluated:

Quantum Kernel + QSVC
Variational Quantum Classifier

Both approaches used the same eight-feature representation and train/test split established by Phase 13.

The quantum-kernel experiment produced:

Accuracy: 0.7586
ROC-AUC: 0.7391
True positives: 0
False negatives: 6

The VQC experiment produced:

Accuracy: 0.6897
ROC-AUC: 0.3442
True positives: 0
False negatives: 6

Both experiments successfully generated reproducible model artifacts, evaluation results, quantum-specific metadata, and automated validation results.

The Phase 15 test suite achieved:

11/11 tests passed

These results demonstrate that the complete QML research pipeline can be executed on the EAG Phase 13 feature space.

They do not establish quantum advantage, production superiority, or real-world generalization.

The outcome of Phase 15 is experimental evidence and reproducible artifacts for Phase 16, where the quantum results will be formally compared with the Phase 14 classical ML results.
