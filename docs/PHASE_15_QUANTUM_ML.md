**# Phase 15 — Quantum Machine Learning Research Lab**



**## 1. Phase Overview**



**Phase 15 introduces a controlled Quantum Machine Learning (QML) research experiment into Extension AI Guard (EAG).**



**The purpose is to investigate whether quantum machine-learning approaches can learn the same binary network-traffic classification problem represented by the frozen Phase 13 feature space, and to measure their performance, computational characteristics, reproducibility, and limitations against classical baselines.**



**This phase is a research and experimentation phase. It does not select the final EAG production model.**



**---**



**## 2. Relationship to the EAG Roadmap**



**The Phase 15 workflow is:**



**```text**

**Phase 12**

**Frozen Dataset**

&#x20;    **↓**

**Phase 13**

**Dataset Preprocessing**

&#x20;    **↓**

**Phase 14**

**Classical ML Baselines**

&#x20;    **↓**

**Phase 15**

**Quantum ML Research Lab**

&#x20;    **↓**

**Phase 16**

**Classical vs Quantum Comparison**

&#x20;    **↓**

**Phase 17**

**Model Evaluation**

**```**



**Phase 15 must use the same processed dataset and train/test split established in Phase 13 so that later comparisons remain controlled.**



**---**



**## 3. Phase 13 Input Contract**



**Phase 15 consumes the verified Phase 13 artifacts.**



**Training set:**



**\* 115 samples**

**\* 89 BENIGN**

**\* 26 MALICIOUS**



**Testing set:**



**\* 29 samples**

**\* 23 BENIGN**

**\* 6 MALICIOUS**



**Processed feature count:**



**\* 8 features**



**Feature mapping:**



**1. `time\_relative`**

**2. `frame\_len`**

**3. `protocol\_HTTP`**

**4. `protocol\_HTTP\_JSON`**

**5. `protocol\_TCP`**

**6. `http\_method\_GET`**

**7. `http\_method\_POST`**

**8. `http\_method\_MISSING`**



**Label mapping:**



**```text**

**BENIGN = 0**

**MALICIOUS = 1**

**```**



**Random state:**



**```text**

**42**

**```**



**Phase 13 preprocessing artifacts must be reused rather than independently recreated.**



**---**



**## 4. Research Question**



**The primary research question is:**



**> Can quantum machine-learning methods learn the EAG binary traffic-classification problem represented by the Phase 13 feature space, and how do their observed predictive and computational characteristics compare with established classical baselines?**



**The experiment must distinguish measured results from theoretical expectations.**



**---**



**## 5. Research Principles**



**Phase 15 follows these principles:**



**\* Same dataset**

**\* Same train/test split**

**\* Same labels**

**\* Same feature contract**

**\* Reproducible configuration**

**\* Simulator-first execution**

**\* Controlled experiments**

**\* Explicit quantum-resource measurements**

**\* No test-set tuning**

**\* No unsupported quantum-advantage claims**

**\* Clear documentation of limitations**



**The objective is to produce a defensible QML research experiment rather than artificially maximize a score.**



**---**



**## 6. Selected Quantum ML Approaches**



**Two QML approaches will be investigated.**



**### 6.1 Primary: Quantum Kernel + QSVC**



**The classical feature vector is mapped into a quantum state using a quantum feature map.**



**Quantum-state similarity is then used to construct a kernel matrix.**



**The resulting quantum kernel is supplied to a Support Vector Classifier.**



**Pipeline:**



**```text**

**Classical Features**

&#x20;       **↓**

**Quantum Feature Map**

&#x20;       **↓**

**Quantum States**

&#x20;       **↓**

**Quantum Kernel**

&#x20;       **↓**

**Kernel Matrix**

&#x20;       **↓**

**QSVC**

&#x20;       **↓**

**BENIGN / MALICIOUS**

**```**



**The quantum-kernel experiment is the primary QML experiment.**



**### 6.2 Secondary: Variational Quantum Classifier**



**A Variational Quantum Classifier (VQC) will provide a second QML approach.**



**Pipeline:**



**```text**

**Classical Features**

&#x20;       **↓**

**Quantum Feature Map**

&#x20;       **↓**

**Parameterized Quantum Circuit**

&#x20;       **↓**

**Measurement**

&#x20;       **↓**

**Optimization**

&#x20;       **↓**

**Classification**

&#x20;       **↓**

**BENIGN / MALICIOUS**

**```**



**The VQC experiment must record optimization and trainability information in addition to ordinary classification metrics.**



**---**



**## 7. Classical Control**



**The quantum-kernel experiment will include a matched classical RBF SVM control.**



**The control must use:**



**\* Same Phase 13 data**

**\* Same train/test split**

**\* Same preprocessing**

**\* Random state 42 where applicable**

**\* No test-set tuning**



**The purpose is to determine whether observed QML behavior is meaningfully different from a strong classical kernel baseline.**



**---**



**## 8. Quantum Framework**



**The primary framework will be:**



**\* Qiskit**

**\* Qiskit Machine Learning**



**The actual installed versions must be verified before implementation and recorded in the experiment metadata.**



**The implementation must not assume that a proposed version is installed until compatibility has been tested in the EAG environment.**



**---**



**## 9. Simulator-First Strategy**



**Phase 15 will initially run on a local simulator.**



**Reasons:**



**\* Reproducibility**

**\* Deterministic debugging**

**\* No cloud dependency**

**\* No hardware queue dependency**

**\* Easier automated testing**

**\* Controlled experimentation**



**Real quantum hardware is optional.**



**If real hardware is used, it must be documented separately with backend name, execution configuration, shots, date/time, and relevant resource information.**



**---**



**## 10. Feature Encoding Strategy**



**The initial encoding strategy will use angle-based encoding.**



**The eight processed features will be mapped into quantum rotation parameters.**



**Initial conceptual mapping:**



**```text**

**x1 → rotation**

**x2 → rotation**

**x3 → rotation**

**...**

**x8 → rotation**

**```**



**A shallow entanglement configuration will be investigated as the initial controlled circuit design.**



**Alternative encoding or circuit configurations may be investigated only as controlled experiments and must be recorded in the experiment metadata.**



**---**



**## 11. Qubit Strategy**



**The initial candidate configuration is:**



**```text**

**8 processed features**

&#x20;       **↓**

**8 initial qubits**

**```**



**However, the number of features does not inherently require one qubit per feature.**



**If dimensionality reduction or another encoding strategy is later tested, it must be explicitly documented and compared rather than silently replacing the original configuration.**



**---**



**## 12. Quantum Kernel Experiment**



**The quantum-kernel experiment will:**



**1. Load the Phase 13 processed training data.**

**2. Load the Phase 13 processed test data.**

**3. Construct the quantum feature map.**

**4. Generate the quantum kernel.**

**5. Calculate the training kernel matrix.**

**6. Calculate the test kernel matrix.**

**7. Train QSVC.**

**8. Predict the test set.**

**9. Calculate classification metrics.**

**10. Record quantum-resource and execution information.**

**11. Save the trained artifact and experiment metadata.**



**Kernel integrity checks must include:**



**\* Matrix dimensions**

**\* Symmetry**

**\* Diagonal behavior**

**\* Finite values**

**\* No NaN values**

**\* No infinite values**

**\* Reproducibility**



**---**



**## 13. VQC Experiment**



**The VQC experiment will record:**



**\* Feature map**

**\* Ansatz**

**\* Number of qubits**

**\* Circuit depth**

**\* Number of trainable parameters**

**\* Optimizer**

**\* Initialization strategy**

**\* Training convergence**

**\* Loss behavior**

**\* Training time**

**\* Inference time**

**\* Classification metrics**



**The VQC must be executed using the same Phase 13 train/test contract.**



**---**



**## 14. Trainability and Barren-Plateau Awareness**



**Phase 15 will investigate trainability-related characteristics without automatically claiming the presence or absence of barren plateaus.**



**The experiment may record:**



**\* Circuit depth**

**\* Number of trainable parameters**

**\* Optimization behavior**

**\* Loss progression**

**\* Convergence behavior**

**\* Gradient-related observations where practical**



**Any barren-plateau conclusion must be supported by measured evidence.**



**---**



**## 15. Metrics**



**Standard classification metrics will include:**



**\* Accuracy**

**\* Precision**

**\* Recall**

**\* F1-score**

**\* ROC-AUC**

**\* False positives**

**\* False negatives**

**\* Confusion matrix**



**Quantum-specific measurements will include, where applicable:**



**\* Qubit count**

**\* Circuit depth**

**\* Parameter count**

**\* Feature-map configuration**

**\* Ansatz configuration**

**\* Kernel construction cost**

**\* Circuit execution count**

**\* Training time**

**\* Inference time**

**\* Backend/simulator information**



**---**



**## 16. Reproducibility Metadata**



**Every experiment must record sufficient metadata to reproduce the result.**



**Metadata should include:**



**\* EAG phase**

**\* Experiment ID**

**\* Timestamp**

**\* Dataset source**

**\* Training sample count**

**\* Testing sample count**

**\* Feature count**

**\* Label mapping**

**\* Random state**

**\* Python version**

**\* Qiskit version**

**\* Qiskit Machine Learning version**

**\* Feature-map configuration**

**\* Ansatz configuration**

**\* Qubit count**

**\* Circuit depth**

**\* Parameter count**

**\* Optimizer**

**\* Number of shots where applicable**

**\* Backend or simulator**

**\* Model type**

**\* Configuration details**



**---**



**## 17. Proposed Directory Structure**



**```text**

**ml/**

**└── quantum/**

&#x20;   **├── README.md**

&#x20;   **├── quantum\_config.py**

&#x20;   **├── feature\_maps.py**

&#x20;   **├── quantum\_kernel.py**

&#x20;   **├── train\_qsvc.py**

&#x20;   **├── train\_vqc.py**

&#x20;   **├── evaluate\_quantum\_models.py**

&#x20;   **├── benchmark\_quantum\_models.py**

&#x20;   **├── generate\_quantum\_metrics.py**

&#x20;   **├── test\_quantum\_ml.py**

&#x20;   **│**

&#x20;   **├── artifacts/**

&#x20;   **│   ├── quantum\_kernel/**

&#x20;   **│   └── vqc/**

&#x20;   **│**

&#x20;   **└── results/**

&#x20;       **├── quantum\_ml\_evaluation.csv**

&#x20;       **├── quantum\_ml\_metrics.json**

&#x20;       **└── experiment\_metadata.json**

**```**



**The directory will be created only after the Phase 15 design has been committed.**



**---**



**## 18. Proposed Experiments**



**### Experiment A — Quantum Kernel + QSVC**



**Measure:**



**\* Classification performance**

**\* Kernel integrity**

**\* Kernel construction cost**

**\* Circuit resources**

**\* Reproducibility**



**### Experiment B — VQC**



**Measure:**



**\* Classification performance**

**\* Training convergence**

**\* Circuit resources**

**\* Parameter count**

**\* Training and inference cost**



**### Experiment C — Classical RBF SVM Control**



**Measure:**



**\* Classification performance**

**\* Training cost**

**\* Inference cost**



**The control provides a matched reference for interpreting the quantum-kernel experiment.**



**---**



**## 19. Fair Experimental Comparison**



**Phase 15 must not modify the dataset to make QML appear stronger.**



**The following must remain consistent:**



**```text**

**Dataset**

&#x20;   **↓**

**Preprocessing**

&#x20;   **↓**

**Train/Test Split**

&#x20;   **↓**

**Labels**

**```**



**No test-set optimization is permitted.**



**Hyperparameter changes must be documented.**



**Any alternative experiment must be clearly identified as an additional experiment rather than silently replacing the primary configuration.**



**---**



**## 20. Artifacts**



**Expected Phase 15 artifacts include:**



**```text**

**Quantum model artifacts**

&#x20;       **↓**

**Evaluation results**

&#x20;       **↓**

**Quantum-specific metrics**

&#x20;       **↓**

**Experiment metadata**

&#x20;       **↓**

**Automated tests**

&#x20;       **↓**

**Phase 15 documentation**

**```**



**Artifacts must be reproducible and traceable to the experiment configuration that produced them.**



**---**



**## 21. Testing Requirements**



**Automated tests must verify at minimum:**



**\* Phase 13 input artifacts exist.**

**\* Expected feature count is 8.**

**\* Expected train/test dimensions are maintained.**

**\* Labels are valid.**

**\* No processed input contains missing values.**

**\* Quantum feature-map construction works.**

**\* Quantum kernel dimensions are correct.**

**\* Quantum kernel contains finite values.**

**\* Kernel integrity checks pass.**

**\* QSVC can train and predict.**

**\* VQC configuration is valid.**

**\* Expected result artifacts are generated.**

**\* Metadata contains required fields.**

**\* Saved artifacts can be loaded.**



**All tests must pass before Phase 15 is considered complete.**



**---**



**## 22. Security and Leakage Controls**



**Phase 13 leakage controls remain mandatory.**



**The following lab-specific identifiers must not be reintroduced as model features:**



**\* Raw IP addresses**

**\* Frame numbers**

**\* Raw HTTP URI**

**\* Capture-specific port identifiers**



**The purpose is to prevent the quantum model from memorizing the controlled laboratory environment.**



**---**



**## 23. Dataset Limitations**



**The current dataset is intentionally small:**



**```text**

**144 total samples**

**115 training samples**

**29 testing samples**

**```**



**The test set contains only:**



**```text**

**23 BENIGN**

**6 MALICIOUS**

**```**



**Therefore, Phase 15 results must not be interpreted as evidence of real-world generalization.**



**The controlled laboratory dataset is suitable for demonstrating the research pipeline, not for proving production-level detection performance.**



**---**



**## 24. No Quantum Advantage Claim**



**Phase 15 must not claim:**



**\* Quantum advantage**

**\* Quantum supremacy**

**\* Production superiority**

**\* Real-world superiority**

**\* Guaranteed generalization**

**\* Faster classification than classical ML**



**Such conclusions require appropriate evidence and experimental scale.**



**Observed performance differences must be reported as experimental results under the specific Phase 15 configuration.**



**---**



**## 25. Real Hardware Policy**



**Real QPU execution is optional.**



**If performed, the following must be recorded:**



**\* Hardware backend**

**\* Date/time**

**\* Number of shots**

**\* Circuit configuration**

**\* Qubit configuration**

**\* Transpilation information where relevant**

**\* Execution cost/time**

**\* Result differences from simulation**



**Simulator results remain the primary reproducible baseline unless hardware experiments are separately documented.**



**---**



**## 26. Phase 15 Completion Criteria**



**Phase 15 is complete only when:**



**\* \[ ] Phase 15 documentation is committed.**

**\* \[ ] Qiskit environment is verified.**

**\* \[ ] Phase 13 input contract is verified.**

**\* \[ ] Quantum feature encoding is implemented and tested.**

**\* \[ ] Quantum Kernel + QSVC is implemented.**

**\* \[ ] VQC is implemented.**

**\* \[ ] Classical RBF SVM control is implemented.**

**\* \[ ] Quantum experiments execute successfully.**

**\* \[ ] Classification metrics are generated.**

**\* \[ ] Quantum-specific metrics are generated.**

**\* \[ ] Experiment metadata is generated.**

**\* \[ ] Model/artifact files are saved.**

**\* \[ ] Automated tests pass.**

**\* \[ ] Results and limitations are documented.**

**\* \[ ] No unsupported quantum-advantage claim is made.**

**\* \[ ] Phase 16 handoff is documented.**

**\* \[ ] Git working tree is clean.**

**\* \[ ] Phase 15 changes are committed and pushed.**



**---**



**## 27. Phase 16 Handoff**



**Phase 15 will provide the following inputs to Phase 16:**



**```text**

**Phase 14 Classical ML Results**

&#x20;       **+**

**Phase 15 Quantum ML Results**

&#x20;       **↓**

**Phase 16 Formal Model Comparison**

**```**



**Phase 16 will perform the formal comparison.**



**Phase 15 itself will not declare a final production model.**



**---**



**## 28. Research Conclusion**



**Phase 15 establishes a controlled and reproducible Quantum Machine Learning research track for Extension AI Guard.**



**The experiment will investigate Quantum Kernel + QSVC and VQC using the same feature space and train/test split established in Phase 13, while maintaining a classical RBF SVM control and recording both conventional ML metrics and quantum-specific resource measurements.**



**The outcome of this phase is experimental evidence and reproducible artifacts for Phase 16, not a predetermined claim that quantum machine learning is superior to classical machine learning.**