**# Phase 16 — Classical vs Quantum Model Comparison Report**



**## 1. Executive Summary**



**Phase 16 performs the formal comparison between the classical machine-learning models evaluated in Phase 14 and the quantum machine-learning models evaluated in Phase 15.**



**The comparison uses the same Phase 13 preprocessing contract, including the same processed feature space, labels, and train/test split.**



**No models are retrained during Phase 16, and no test-set tuning is performed.**



**The purpose of this phase is to document the measured predictive and computational characteristics of the models and provide controlled evidence for the Phase 17 evaluation stage.**



**Phase 16 does not declare a production model and does not claim quantum advantage, quantum supremacy, or real-world quantum superiority.**



**---**



**## 2. Dataset and Experimental Contract**



**The comparison is based on the frozen Phase 13 experiment contract.**



**### Dataset**



**Total samples:**



**```text**

**144**

**```**



**Training samples:**



**```text**

**115**

**```**



**Testing samples:**



**```text**

**29**

**```**



**Training labels:**



**```text**

**BENIGN    = 89**

**MALICIOUS = 26**

**```**



**Testing labels:**



**```text**

**BENIGN    = 23**

**MALICIOUS = 6**

**```**



**Processed feature count:**



**```text**

**8**

**```**



**Label mapping:**



**```text**

**BENIGN    = 0**

**MALICIOUS = 1**

**```**



**Random state:**



**```text**

**42**

**```**



**The comparison therefore evaluates the models under a common experimental contract.**



**---**



**## 3. Models Compared**



**### Classical Models**



**Phase 14 produced results for:**



**1. Logistic Regression**

**2. Decision Tree**

**3. Random Forest**

**4. SVM**

**5. KNN**

**6. Gradient Boosting**



**### Quantum Models**



**Phase 15 produced results for:**



**1. Quantum Support Vector Classifier (QSVC)**

**2. Variational Quantum Classifier (VQC)**



**Total models compared:**



**```text**

**8**

**```**



**---**



**## 4. Predictive Results**



**The following values are measured results from Phases 14 and 15.**



**| Model               | Family    | Accuracy | Precision | Recall |     F1 | ROC-AUC | FP | FN |**

**| ------------------- | --------- | -------: | --------: | -----: | -----: | ------: | -: | -: |**

**| Logistic Regression | Classical |   0.8276 |    1.0000 | 0.1667 | 0.2857 |  0.7681 |  0 |  5 |**

**| Decision Tree       | Classical |   0.8276 |    0.5714 | 0.6667 | 0.6154 |  0.7609 |  3 |  2 |**

**| Random Forest       | Classical |   0.7586 |    0.4286 | 0.5000 | 0.4615 |  0.7572 |  4 |  3 |**

**| SVM                 | Classical |   0.8276 |    1.0000 | 0.1667 | 0.2857 |  0.7681 |  0 |  5 |**

**| KNN                 | Classical |   0.8276 |    0.6000 | 0.5000 | 0.5455 |  0.6558 |  2 |  3 |**

**| Gradient Boosting   | Classical |   0.8276 |    0.5556 | 0.8333 | 0.6667 |  0.9058 |  4 |  1 |**

**| QSVC                | Quantum   |   0.7586 |    0.0000 | 0.0000 | 0.0000 |  0.7391 |  1 |  6 |**

**| VQC                 | Quantum   |   0.6897 |    0.0000 | 0.0000 | 0.0000 |  0.3442 |  3 |  6 |**



**These values are reported exactly from the existing Phase 14 and Phase 15 evaluation artifacts.**



**---**



**## 5. Interpretation of Predictive Measurements**



**The measurements show that the classical models produced non-zero malicious-class recall on the Phase 13 test set, while the evaluated QSVC and VQC configurations produced zero malicious-class recall.**



**For the classical experiments, the measured results varied substantially between models.**



**Gradient Boosting produced:**



**```text**

**Accuracy  = 0.8276**

**Recall    = 0.8333**

**F1        = 0.6667**

**ROC-AUC   = 0.9058**

**FP        = 4**

**FN        = 1**

**```**



**The quantum-kernel QSVC experiment produced:**



**```text**

**Accuracy  = 0.7586**

**Recall    = 0.0000**

**F1        = 0.0000**

**ROC-AUC   = 0.7391**

**FP        = 1**

**FN        = 6**

**```**



**The VQC experiment produced:**



**```text**

**Accuracy  = 0.6897**

**Recall    = 0.0000**

**F1        = 0.0000**

**ROC-AUC   = 0.3442**

**FP        = 3**

**FN        = 6**

**```**



**These observations describe this specific experiment and should not be generalized to quantum machine learning as a whole.**



**---**



**## 6. Computational Characteristics**



**The measured Phase 14 classical training times were:**



**| Model               | Training Time (seconds) |**

**| ------------------- | ----------------------: |**

**| Logistic Regression |                0.036843 |**

**| Decision Tree       |                0.002781 |**

**| Random Forest       |                0.094974 |**

**| SVM                 |                0.038528 |**

**| KNN                 |                0.002460 |**

**| Gradient Boosting   |                0.074427 |**



**The Phase 15 quantum training times were:**



**| Model | Training Time (seconds) |**

**| ----- | ----------------------: |**

**| QSVC  |               28.624561 |**

**| VQC   |               41.913872 |**



**The quantum experiments therefore involved substantially greater measured training time in this local simulator configuration.**



**This observation concerns the implemented simulator-based experiment and is not a general statement about all quantum hardware or quantum algorithms.**



**---**



**## 7. Inference Characteristics**



**Measured classical inference time per test sample:**



**| Model               | Inference / Sample |**

**| ------------------- | -----------------: |**

**| Logistic Regression |        0.532666 ms |**

**| Decision Tree       |        0.057424 ms |**

**| Random Forest       |        0.229959 ms |**

**| SVM                 |        0.081493 ms |**

**| KNN                 |        0.191207 ms |**

**| Gradient Boosting   |        0.070945 ms |**



**Measured quantum inference time per test sample:**



**| Model | Inference / Sample |**

**| ----- | -----------------: |**

**| QSVC  |      583.026338 ms |**

**| VQC   |        4.629493 ms |**



**The QSVC inference measurement includes the cost associated with the quantum-kernel evaluation performed by the simulator-based implementation.**



**The VQC inference measurement is substantially lower than QSVC inference in this experiment, although it remains higher than the measured classical inference times.**



**---**



**## 8. QSVC Quantum Resource Characteristics**



**The primary quantum-kernel experiment used:**



**```text**

**Feature map:**

**ZZFeatureMap**



**Qubits:**

**8**



**Feature-map parameters:**

**8**



**Circuit depth:**

**23**



**Circuit size:**

**37**



**Entanglement:**

**linear**



**Repetitions:**

**1**

**```**



**The quantum kernel was constructed from the encoded feature vectors.**



**Kernel matrix:**



**```text**

**Shape:**

**115 × 115**

**```**



**Measured kernel statistics:**



**```text**

**Minimum:**

**0.000000016760**



**Maximum:**

**1.000000000004**



**Mean:**

**0.258488765979**



**Mean diagonal:**

**1.000000000002**

**```**



**Integrity checks confirmed:**



**```text**

**Finite values:**

**True**



**Symmetric:**

**True**



**Diagonal approximately one:**

**True**

**```**



**The kernel matrix therefore passed the Phase 15 integrity checks.**



**---**



**## 9. QSVC Computational Cost**



**The QSVC experiment required:**



**```text**

**Training time:**

**28.624561 seconds**

**```**



**Total test inference time:**



**```text**

**16.907764 seconds**

**```**



**Inference time per test sample:**



**```text**

**583.026338 ms**

**```**



**The model was also saved and independently reloaded successfully.**



**Support-vector information recorded during the experiment was:**



**```text**

**Support vectors:**

**\[40, 26]**

**```**



**These values are experimental measurements from the Phase 15 simulator configuration.**



**---**



**## 10. VQC Resource Characteristics**



**The VQC experiment used the same eight-feature input contract.**



**The experiment recorded:**



**```text**

**Qubits:**

**8**



**Feature map:**

**ZZFeatureMap**



**Ansatz:**

**RealAmplitudes**



**Optimizer:**

**COBYLA**



**Sampler:**

**Statevector sampler**



**Default shots:**

**1024**



**Random state:**

**42**

**```**



**The VQC experiment used a custom loss-tracking optimizer wrapper so that optimization history could be preserved for later analysis.**



**Measured training characteristics:**



**```text**

**Training time:**

**41.913872 seconds**



**Objective evaluations:**

**100**



**Initial loss:**

**1.228184916450**



**Final loss:**

**0.966805365648**



**Minimum loss:**

**0.965840828639**

**```**



**The trained model was successfully saved and independently reloaded.**



**---**



**## 11. VQC Trainability Observations**



**The VQC optimization process showed measurable loss reduction during the experiment.**



**However, the experiment does not provide sufficient evidence to make a general claim about trainability of VQCs.**



**In particular, the Phase 16 results do not establish the presence or absence of a barren plateau.**



**The appropriate conclusion is limited to the observed optimization behavior of this specific circuit, optimizer, initialization, simulator, dataset, and training configuration.**



**---**



**## 12. Classical vs Quantum Resource Comparison**



**The experiments show different computational characteristics.**



**The classical models operated directly on the eight-dimensional processed feature space.**



**The quantum models encoded those features into an eight-qubit quantum circuit.**



**The quantum-kernel method additionally required construction and evaluation of a kernel matrix.**



**Therefore, the measured computational workload is not directly equivalent to a classical model requiring only a conventional feature-vector evaluation.**



**The comparison should consequently consider:**



**\* predictive measurements**

**\* training time**

**\* inference time**

**\* circuit depth**

**\* qubit count**

**\* parameter count**

**\* kernel construction cost**

**\* simulator execution cost**

**\* optimization behavior**



**rather than treating one metric as sufficient to characterize the models.**



**---**



**## 13. Kernel Construction Considerations**



**The QSVC approach required construction of the training kernel matrix using 115 training samples.**



**A kernel matrix with dimensions:**



**```text**

**115 × 115**

**```**



**contains:**



**```text**

**13,225**

**```**



**matrix entries.**



**The quantum kernel therefore introduces a computational operation that does not appear in the same form in the classical model evaluation pipeline.**



**The measured QSVC training time includes this kernel-based computational workload.**



**---**



**## 14. Fairness of the Comparison**



**Phase 16 did not retrain any model.**



**The comparison consumed the existing Phase 14 and Phase 15 evaluation artifacts.**



**The following remained fixed:**



**```text**

**Dataset**

**Train/test split**

**Feature space**

**Labels**

**Random state**

**```**



**No test-set optimization was performed.**



**No model was selectively removed because of its measured result.**



**No quantum result was modified to improve comparability.**



**The comparison therefore represents the previously executed experiments under their recorded configurations.**



**---**



**## 15. Dataset Size Limitation**



**The dataset contains only:**



**```text**

**144 total samples**

**```**



**with:**



**```text**

**115 training samples**

**29 testing samples**

**```**



**The test set contains only:**



**```text**

**23 BENIGN**

**6 MALICIOUS**

**```**



**This is a very small controlled experimental dataset.**



**Consequently:**



**\* individual test predictions have a large effect on metrics;**

**\* a single false negative changes recall substantially;**

**\* measured differences may not remain stable on larger datasets;**

**\* the experiment does not establish real-world generalization;**

**\* the results should not be interpreted as production detection performance.**



**The purpose of the experiment is controlled research and pipeline validation.**



**---**



**## 16. No Quantum Advantage Claim**



**Phase 16 does not claim:**



**\* Quantum advantage**

**\* Quantum supremacy**

**\* Production superiority**

**\* Real-world superiority**

**\* Guaranteed generalization**

**\* Faster classification by quantum machine learning**



**The measured results only describe the tested configurations.**



**A defensible quantum-advantage claim would require substantially broader evidence, appropriate baselines, representative workloads, and carefully controlled hardware or computational resource comparisons.**



**---**



**## 17. Research Interpretation**



**The Phase 16 measurements demonstrate that both classical and quantum machine-learning pipelines can be executed using the common EAG feature space.**



**The evaluated classical configurations produced measurable malicious-class predictions on the test set.**



**The evaluated QSVC and VQC configurations did not correctly classify any malicious test samples under their recorded configurations.**



**The quantum experiments also incurred higher measured training cost in the simulator environment.**



**These observations provide useful evidence for Phase 17 but do not establish a universal performance ordering between classical and quantum machine learning.**



**---**



**## 18. Reproducibility**



**The comparison is reproducible from the stored Phase 14 and Phase 15 artifacts.**



**Phase 16 records:**



**```text**

**Phase:**

**16**



**Experiment:**

**classical\_vs\_quantum\_model\_comparison**



**Random state:**

**42**



**Retraining:**

**False**



**Test-set tuning:**

**False**

**```**



**The comparison artifacts are generated from the existing evaluation files rather than from newly trained models.**



**---**



**## 19. Generated Artifacts**



**Phase 16 generates:**



**```text**

**ml/comparison/**

**├── compare\_models.py**

**├── test\_phase16.py**

**│**

**├── results/**

**│   ├── model\_comparison.csv**

**│   ├── model\_comparison.json**

**│   └── comparison\_metadata.json**

**│**

**└── reports/**

&#x20;   **└── PHASE\_16\_COMPARISON\_REPORT.md**

**```**



**The CSV provides machine-readable comparison data.**



**The JSON file provides structured comparison data.**



**The metadata file records the experimental contract and comparison conditions.**



**This report provides the human-readable interpretation of the measurements.**



**---**



**## 20. Validation**



**The Phase 16 automated validation suite contains 14 tests.**



**The latest execution produced:**



**```text**

**Ran 14 tests in 0.018s**



**OK**

**```**



**The validation checks include:**



**\* comparison directory existence;**

**\* comparison CSV existence;**

**\* comparison JSON existence;**

**\* metadata existence;**

**\* required columns;**

**\* expected model count;**

**\* phase mapping;**

**\* finite metric values;**

**\* valid error counts;**

**\* unique model names;**

**\* JSON/CSV consistency;**

**\* metadata contract;**

**\* absence of unsupported quantum-advantage claims;**

**\* preservation of measured Phase 14 and Phase 15 results.**



**---**



**## 21. Phase 17 Handoff**



**Phase 16 provides the following inputs to Phase 17:**



**```text**

**Phase 14 Classical ML Results**

&#x20;            **+**

**Phase 15 Quantum ML Results**

&#x20;            **+**

**Phase 16 Formal Comparison**

&#x20;            **↓**

**Phase 17 Model Evaluation**

**```**



**Phase 17 should focus on formal evaluation of model behavior, limitations, error characteristics, and suitability for the EAG detection objective.**



**Phase 17 must continue to respect the frozen Phase 13 data contract and must not retroactively modify earlier experiments to improve results.**



**---**



**## 22. Conclusion**



**Phase 16 establishes a reproducible comparison layer between the classical and quantum machine-learning experiments performed in EAG.**



**The comparison demonstrates measurable differences in predictive behavior, training cost, inference characteristics, quantum resources, kernel construction, and VQC optimization behavior.**



**Under the specific recorded experiment configurations, the quantum models did not reproduce the malicious-class detection observed by several classical models.**



**However, the small controlled dataset and simulator-based execution substantially limit the conclusions that can be drawn.**



**The results should therefore be treated as experimental evidence for the EAG research pipeline rather than evidence of universal superiority of either computational paradigm.**



**Phase 16 provides the documented comparison artifacts required for the Phase 17 evaluation stage.**



