**# Phase 16 — Classical vs Quantum Model Comparison**



**## 1. Phase Overview**



**Phase 16 formally compares the classical machine-learning results produced in Phase 14 with the Quantum Machine Learning results produced in Phase 15.**



**The purpose of this phase is to provide a controlled, reproducible comparison of predictive performance and computational characteristics without changing the frozen Phase 13 dataset, preprocessing pipeline, or train/test split.**



**Phase 16 does not introduce a new production model. The formal evaluation and production-model decision remain part of Phase 17.**



**---**



**## 2. Relationship to the EAG Roadmap**



**```text**

**Phase 13**

**Frozen Preprocessed Dataset**

&#x20;       **↓**

**Phase 14**

**Classical ML Results**

&#x20;       **+**

**Phase 15**

**Quantum ML Results**

&#x20;       **↓**

**Phase 16**

**Classical vs Quantum Comparison**

&#x20;       **↓**

**Phase 17**

**Formal Model Evaluation**

&#x20;       **↓**

**Phase 18**

**Real-Time Detection Engine**

**```**



**Phase 16 consumes the completed results from Phases 14 and 15.**



**Previously generated models and evaluation results must be reused rather than independently recreated.**



**---**



**## 3. Phase 13 Comparison Contract**



**All model results originate from the same Phase 13 dataset contract.**



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



**Labels:**



**```text**

**BENIGN = 0**

**MALICIOUS = 1**

**```**



**Random state:**



**```text**

**42**

**```**



**The Phase 13 preprocessing artifacts remain frozen.**



**---**



**## 4. Models Being Compared**



**### 4.1 Classical Models**



**Phase 14 produced results for:**



**1. Logistic Regression**

**2. Decision Tree**

**3. Random Forest**

**4. SVM**

**5. KNN**

**6. Gradient Boosting**



**### 4.2 Quantum Models**



**Phase 15 produced results for:**



**1. Quantum Kernel + QSVC**

**2. Variational Quantum Classifier (VQC)**



**The quantum models remain research models and are not automatically considered production models.**



**---**



**## 5. Predictive Metrics**



**Phase 16 compares:**



**\* Accuracy**

**\* Precision**

**\* Recall**

**\* F1-score**

**\* ROC-AUC**

**\* False positives**

**\* False negatives**

**\* True positives**

**\* True negatives**



**Because the test set contains only six MALICIOUS samples, individual classification errors can substantially affect percentage-based metrics.**



**Therefore, metric differences must be interpreted in the context of the small evaluation dataset.**



**---**



**## 6. Classical Model Results**



**Phase 14 produced the following results.**



**| Model               | Accuracy | Precision | Recall |     F1 | ROC-AUC | FP | FN |**

**| ------------------- | -------: | --------: | -----: | -----: | ------: | -: | -: |**

**| Logistic Regression |   0.8276 |    1.0000 | 0.1667 | 0.2857 |  0.7681 |  0 |  5 |**

**| Decision Tree       |   0.8276 |    0.5714 | 0.6667 | 0.6154 |  0.7609 |  3 |  2 |**

**| Random Forest       |   0.7586 |    0.4286 | 0.5000 | 0.4615 |  0.7572 |  4 |  3 |**

**| SVM                 |   0.8276 |    1.0000 | 0.1667 | 0.2857 |  0.7681 |  0 |  5 |**

**| KNN                 |   0.8276 |    0.6000 | 0.5000 | 0.5455 |  0.6558 |  2 |  3 |**

**| Gradient Boosting   |   0.8276 |    0.5556 | 0.8333 | 0.6667 |  0.9058 |  4 |  1 |**



**These values are imported from the completed Phase 14 results.**



**---**



**## 7. Quantum Model Results**



**Phase 15 produced the following results.**



**| Model | Accuracy | Precision | Recall |     F1 | ROC-AUC | FP | FN |**

**| ----- | -------: | --------: | -----: | -----: | ------: | -: | -: |**

**| QSVC  |   0.7586 |    0.0000 | 0.0000 | 0.0000 |  0.7391 |  1 |  6 |**

**| VQC   |   0.6897 |    0.0000 | 0.0000 | 0.0000 |  0.3442 |  3 |  6 |**



**Confusion matrices:**



**### QSVC**



**```text**

&#x20;               **Predicted**

&#x20;             **BENIGN  MALICIOUS**

**Actual BENIGN     22       1**

&#x20;      **MALICIOUS   6       0**

**```**



**### VQC**



**```text**

&#x20;               **Predicted**

&#x20;             **BENIGN  MALICIOUS**

**Actual BENIGN     20       3**

&#x20;      **MALICIOUS   6       0**

**```**



**These results represent the specific simulator-based Phase 15 configurations and should not be generalized beyond this experiment.**



**---**



**## 8. Computational Characteristics**



**Phase 16 also compares computational behavior.**



**### Classical training time**



**| Model               | Training time |**

**| ------------------- | ------------: |**

**| Logistic Regression |    0.036843 s |**

**| Decision Tree       |    0.002781 s |**

**| Random Forest       |    0.094974 s |**

**| SVM                 |    0.038528 s |**

**| KNN                 |    0.002460 s |**

**| Gradient Boosting   |    0.074427 s |**



**### Quantum training time**



**| Model | Training time |**

**| ----- | ------------: |**

**| QSVC  |   28.624561 s |**

**| VQC   |   41.913872 s |**



**These values are experiment measurements under the Phase 14 and Phase 15 configurations.**



**Training-time comparisons must account for the fundamentally different computation performed by the quantum simulator and classical algorithms.**



**---**



**## 9. Inference Characteristics**



**Phase 14 recorded the following inference time per test sample:**



**| Model               | Inference time/sample |**

**| ------------------- | --------------------: |**

**| Logistic Regression |           0.532666 ms |**

**| Decision Tree       |           0.057424 ms |**

**| Random Forest       |           0.229959 ms |**

**| SVM                 |           0.081493 ms |**

**| KNN                 |           0.191207 ms |**

**| Gradient Boosting   |           0.070945 ms |**



**Phase 15 recorded:**



**| Model | Inference time/sample |**

**| ----- | --------------------: |**

**| QSVC  |         583.026338 ms |**

**| VQC   |           4.629493 ms |**



**QSVC inference includes quantum-kernel computation under the simulator configuration and therefore must not be interpreted as a direct prediction of future physical-QPU performance.**



**---**



**## 10. Quantum Resource Characteristics**



**The Phase 15 quantum configuration used:**



**```text**

**Qubits: 8**

**Feature-map repetitions: 1**

**Entanglement: linear**

**Feature-map parameters: 8**

**Feature-map depth: 23**

**Feature-map size: 37**

**VQC ansatz repetitions: 1**

**VQC optimizer: COBYLA**

**VQC maximum iterations: 100**

**Simulator: StatevectorSampler**

**```**



**The quantum kernel matrix had:**



**```text**

**Shape: 115 × 115**

**Minimum: 0.000000016760**

**Maximum: 1.000000000004**

**Mean: 0.258488765979**

**Diagonal mean: 1.000000000002**

**```**



**Kernel integrity checks passed.**



**---**



**## 11. VQC Trainability Characteristics**



**The Phase 15 VQC experiment recorded:**



**```text**

**Objective evaluations: 100**

**Initial loss: 1.228184916450**

**Final loss: 0.966805365648**

**Minimum loss: 0.965840828639**

**```**



**The optimization behavior is recorded as experimental evidence.**



**Phase 16 does not claim the presence or absence of barren plateaus.**



**The small dataset, shallow circuit, limited optimization budget, and simulator configuration constrain the interpretation of trainability observations.**



**---**



**## 12. Comparison Interpretation**



**The results show that the tested classical and quantum configurations behaved differently on the frozen evaluation set.**



**The classical models produced non-zero recall for several configurations, while both tested quantum models produced zero recall on the six MALICIOUS test samples.**



**The classical results also show differences between accuracy and malicious-class recall. For example, Logistic Regression and SVM achieved 0.8276 accuracy but detected only one of the six MALICIOUS samples.**



**Gradient Boosting achieved:**



**```text**

**Accuracy: 0.8276**

**Recall:   0.8333**

**F1:       0.6667**

**ROC-AUC:  0.9058**

**```**



**These values are reported observations from Phase 14 and are not by themselves sufficient to establish production suitability.**



**---**



**## 13. Important Dataset Limitation**



**The evaluation set contains only:**



**```text**

**23 BENIGN**

**6 MALICIOUS**

**```**



**Consequently:**



**\* One classification error can significantly change recall.**

**\* Metric differences may not remain stable on larger datasets.**

**\* Results cannot establish real-world generalization.**

**\* Results cannot establish production superiority.**

**\* Results cannot establish quantum advantage.**



**Phase 17 will address formal evaluation requirements.**



**---**



**## 14. Fairness of Comparison**



**The comparison preserves:**



**```text**

**Same dataset**

&#x20;     **↓**

**Same preprocessing**

&#x20;     **↓**

**Same train/test split**

&#x20;     **↓**

**Same labels**

&#x20;     **↓**

**Independent model results**

**```**



**No test-set tuning is introduced in Phase 16.**



**No Phase 14 or Phase 15 result is modified to improve the comparison.**



**Any future experiment using a different feature representation, hyperparameter configuration, circuit architecture, or dataset must be identified as a separate experiment.**



**---**



**## 15. Quantum vs Classical Resource Interpretation**



**Quantum-resource measurements should be reported separately from ordinary ML performance metrics.**



**Relevant quantum measurements include:**



**\* Qubit count**

**\* Circuit depth**

**\* Feature-map configuration**

**\* Ansatz configuration**

**\* Parameter count**

**\* Kernel matrix construction**

**\* Simulator backend**

**\* Circuit execution behavior**

**\* VQC objective evaluations**



**These measurements describe the experimental configuration and do not constitute evidence of quantum advantage.**



**---**



**## 16. No Quantum Advantage Claim**



**Phase 16 explicitly does not claim:**



**\* Quantum advantage**

**\* Quantum supremacy**

**\* Production superiority**

**\* Faster computation**

**\* Better generalization**

**\* Real-world superiority**



**A valid quantum-advantage claim would require substantially broader evidence, appropriate baselines, meaningful scale, and a suitable comparison of computational resources.**



**The current EAG dataset and simulator experiment are insufficient for such a conclusion.**



**---**



**## 17. Phase 16 Artifacts**



**The comparison implementation will generate:**



**```text**

**ml/**

**└── comparison/**

&#x20;   **├── README.md**

&#x20;   **├── compare\_models.py**

&#x20;   **├── generate\_comparison\_report.py**

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



**The exact directory will be created after this design is committed.**



**---**



**## 18. Testing Requirements**



**Automated tests must verify:**



**\* Phase 14 results are available.**

**\* Phase 15 results are available.**

**\* Expected model count is eight.**

**\* Required metrics exist.**

**\* Numeric values are finite.**

**\* Model names are unique.**

**\* Expected sample counts are preserved.**

**\* Comparison results are generated.**

**\* JSON results are valid.**

**\* Metadata is generated.**

**\* No source results are silently modified.**

**\* Comparison artifacts can be loaded.**



**All Phase 16 tests must pass before the phase is considered complete.**



**---**



**## 19. Reproducibility**



**Phase 16 metadata must record:**



**\* EAG phase**

**\* Experiment ID**

**\* Timestamp**

**\* Phase 14 result source**

**\* Phase 15 result source**

**\* Dataset/test-set contract**

**\* Model names**

**\* Metrics compared**

**\* Software environment**

**\* Comparison configuration**

**\* Result-generation information**



**The comparison must be reproducible from the committed Phase 14 and Phase 15 artifacts.**



**---**



**## 20. Phase 17 Handoff**



**Phase 16 will provide:**



**```text**

**Phase 14 Classical Results**

&#x20;            **+**

**Phase 15 Quantum Results**

&#x20;            **↓**

&#x20;      **Phase 16 Comparison**

&#x20;            **↓**

&#x20;   **Comparison Artifacts**

&#x20;            **↓**

**Phase 17 Formal Evaluation**

**```**



**Phase 17 will perform deeper evaluation and determine which model configurations are appropriate for the next stage of the EAG pipeline.**



**Phase 16 itself does not finalize the production model.**



**---**



**## 21. Completion Criteria**



**Phase 16 will be complete when:**



**\* \[ ] Phase 16 documentation is committed.**

**\* \[ ] Phase 14 results are imported successfully.**

**\* \[ ] Phase 15 results are imported successfully.**

**\* \[ ] Comparison implementation is complete.**

**\* \[ ] Predictive metrics are compared.**

**\* \[ ] Computational characteristics are compared.**

**\* \[ ] Quantum-resource characteristics are documented.**

**\* \[ ] Comparison artifacts are generated.**

**\* \[ ] Automated tests pass.**

**\* \[ ] Comparison report is generated.**

**\* \[ ] Limitations are documented.**

**\* \[ ] No unsupported quantum-advantage claim is made.**

**\* \[ ] Phase 17 handoff is documented.**

**\* \[ ] Git working tree is clean.**

**\* \[ ] Phase 16 changes are committed and pushed.**



**---**



**## 22. Research Conclusion**



**Phase 16 provides a controlled comparison between the classical ML experiments from Phase 14 and the QML experiments from Phase 15.**



**The comparison uses the same frozen Phase 13 evaluation contract and reports both predictive metrics and computational/resource characteristics.**



**The observed Phase 15 quantum configurations did not detect any of the six MALICIOUS test samples, while several Phase 14 classical configurations detected some malicious samples. These observations are limited to the current small controlled dataset and simulator-based experiment.**



**Phase 16 therefore produces comparative evidence rather than a claim of quantum or classical superiority.**



**The results will be passed to Phase 17 for formal model evaluation.**



