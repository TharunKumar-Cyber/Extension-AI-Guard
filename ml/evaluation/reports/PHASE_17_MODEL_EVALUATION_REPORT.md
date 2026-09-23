# Phase 17 â€” Formal Model Evaluation Report



## 1. Evaluation Overview



Phase 17 formally evaluates the classical and quantum machine-learning models produced during Phases 14 and 15.



The evaluation uses the frozen Phase 13 test dataset without retraining, test-set tuning, or modification of the evaluation contract.



The purpose of this phase is to document predictive performance, classification errors, score-based evaluation, inference characteristics, and reproducibility information for the models that will be handed to Phase 18.



Phase 17 does not select a final production model.



---



## 2. Evaluation Contract



The evaluation used the following frozen contract:



| Property | Value |

|---|---|

| Dataset source | Phase 13 processed dataset |

| Test samples | 29 |

| BENIGN samples | 23 |

| MALICIOUS samples | 6 |

| Processed features | 8 |

| Random state | 42 |

| BENIGN label | 0 |

| MALICIOUS label | 1 |

| Test-set tuning | Not permitted |

| Retraining | Not performed |



The eight processed features remain those established by Phase 13:



## 1. `time\_relative`

## 2. `frame\_len`

## 3. `protocol\_HTTP`

## 4. `protocol\_HTTP\_JSON`

## 5. `protocol\_TCP`

## 6. `http\_method\_GET`

## 7. `http\_method\_POST`

## 8. `http\_method\_MISSING`



Leakage controls from Phase 13 remain applicable.



Raw IP addresses, raw URIs, frame numbers, and capture-specific identifiers were not reintroduced.



---



## 3. Evaluated Models



Eight models were formally evaluated.



### Classical Models



## 1. Logistic Regression

## 2. Decision Tree

## 3. Random Forest

## 4. SVM

## 5. KNN

## 6. Gradient Boosting



### Quantum Models



## 7. Quantum Kernel + QSVC

## 8. Variational Quantum Classifier (VQC)



The models were loaded from their previously generated Phase 14 and Phase 15 artifacts.



No model was retrained during Phase 17.



---



## 4. Evaluation Metrics



The evaluation records:



- Accuracy

- Precision

- Recall

- F1-score

- ROC-AUC

- False positives

- False negatives

- True positives

- True negatives

- Specificity

- Average precision where supported

- Per-class metrics

- ROC curve data where supported

- Precision-recall curve data where supported

- Prediction/decision scores where available

- Inference timing

- Error-analysis information



Confusion matrices and per-class results are stored separately as machine-readable artifacts.



---



## 5. Measured Results



The following results were generated from the frozen Phase 13 test set containing 29 samples.



| Model | Accuracy | Precision | Recall | F1-score | ROC-AUC | FP | FN |

|---|---:|---:|---:|---:|---:|---:|---:|

| Logistic Regression | 0.8276 | 1.0000 | 0.1667 | 0.2857 | 0.7681 | 0 | 5 |

| Decision Tree | 0.8276 | 0.5714 | 0.6667 | 0.6154 | 0.7609 | 3 | 2 |

| Random Forest | 0.7586 | 0.4286 | 0.5000 | 0.4615 | 0.7572 | 4 | 3 |

| SVM | 0.8276 | 1.0000 | 0.1667 | 0.2857 | 0.7681 | 0 | 5 |

| KNN | 0.8276 | 0.6000 | 0.5000 | 0.5455 | 0.6558 | 2 | 3 |

| Gradient Boosting | 0.8276 | 0.5556 | 0.8333 | 0.6667 | 0.9058 | 4 | 1 |

| QSVC | 0.7586 | 0.0000 | 0.0000 | 0.0000 | 0.7391 | 1 | 6 |

| VQC | 0.6897 | 0.0000 | 0.0000 | 0.0000 | 0.3442 | 3 | 6 |



These values are measurements from this specific evaluation configuration and dataset.



---



## 6. Classical Model Evaluation



### 6.1 Logistic Regression



Measured results:



- Accuracy: 0.8276

- Precision: 1.0000

- Recall: 0.1667

- F1-score: 0.2857

- ROC-AUC: 0.7681

- False positives: 0

- False negatives: 5



The model produced no false positives on the test set but missed most malicious samples.



---



### 6.2 Decision Tree



Measured results:



- Accuracy: 0.8276

- Precision: 0.5714

- Recall: 0.6667

- F1-score: 0.6154

- ROC-AUC: 0.7609

- False positives: 3

- False negatives: 2



The model identified more malicious samples than Logistic Regression while producing additional false positives.



---



### 6.3 Random Forest



Measured results:



- Accuracy: 0.7586

- Precision: 0.4286

- Recall: 0.5000

- F1-score: 0.4615

- ROC-AUC: 0.7572

- False positives: 4

- False negatives: 3



The measured test-set performance was lower than several other classical models under this configuration.



---



### 6.4 SVM



Measured results:



- Accuracy: 0.8276

- Precision: 1.0000

- Recall: 0.1667

- F1-score: 0.2857

- ROC-AUC: 0.7681

- False positives: 0

- False negatives: 5



Its observed classification pattern on this test set was similar to Logistic Regression.



---



### 6.5 KNN



Measured results:



- Accuracy: 0.8276

- Precision: 0.6000

- Recall: 0.5000

- F1-score: 0.5455

- ROC-AUC: 0.6558

- False positives: 2

- False negatives: 3



The model produced an intermediate balance between false positives and false negatives under the tested configuration.



---



### 6.6 Gradient Boosting



Measured results:



- Accuracy: 0.8276

- Precision: 0.5556

- Recall: 0.8333

- F1-score: 0.6667

- ROC-AUC: 0.9058

- False positives: 4

- False negatives: 1



The model recorded the highest measured recall and ROC-AUC among the evaluated models in this specific test run.



This observation is reported as an experimental result only and does not constitute a production-model selection decision.



---



## 7. Quantum Model Evaluation



### 7.1 Quantum Kernel + QSVC



Measured results:



- Accuracy: 0.7586

- Precision: 0.0000

- Recall: 0.0000

- F1-score: 0.0000

- ROC-AUC: 0.7391

- False positives: 1

- False negatives: 6



The QSVC produced zero true-positive predictions on the 29-sample evaluation set under the Phase 15 configuration.



The measured inference time in this evaluation was approximately:



- 501.624448 ms/sample



This is an observed simulator-based measurement and should not be generalized to quantum hardware or other implementations.



---



### 7.2 Variational Quantum Classifier



Measured results:



- Accuracy: 0.6897

- Precision: 0.0000

- Recall: 0.0000

- F1-score: 0.0000

- ROC-AUC: 0.3442

- False positives: 3

- False negatives: 6



The VQC produced zero true-positive predictions on the evaluation set under the Phase 15 configuration.



The measured inference time in this evaluation was approximately:



- 3.868393 ms/sample



The result reflects the specific simulator, circuit, optimizer, and configuration used during Phase 15.



---



## 8. Inference Characteristics



Measured inference times from the Phase 17 evaluation run were:



| Model | Inference time/sample |

|---|---:|

| Logistic Regression | 0.217217 ms |

| Decision Tree | 0.012714 ms |

| Random Forest | 0.182431 ms |

| SVM | 0.039076 ms |

| KNN | 0.040531 ms |

| Gradient Boosting | 0.019103 ms |

| QSVC | 501.624448 ms |

| VQC | 3.868393 ms |



These values describe the specific local execution environment and should not be interpreted as universal hardware or deployment benchmarks.



---



## 9. Error Analysis



The evaluation explicitly records false positives and false negatives for each model.



The frozen test set contains only six malicious samples.



Consequently, individual classification errors have a large effect on recall and F1-score.



For example, missing one malicious sample changes malicious recall by approximately 16.7 percentage points because:



```text

1 / 6 = 16.7%


Detailed error-analysis information is stored in:



ml/evaluation/results/error\_analysis.json

## 10. Confusion Matrices



The complete confusion matrices are stored in:



ml/evaluation/results/confusion\_matrices.json



The evaluation uses the standard binary classification structure:



&#x20;                   Predicted

&#x20;                BENIGN   MALICIOUS

Actual BENIGN       TN        FP

Actual MALICIOUS    FN        TP



The stored matrices provide the basis for the reported accuracy, precision, recall, F1-score, and specificity values.



## 11. Per-Class Evaluation



Per-class metrics are stored in:



ml/evaluation/results/per\_class\_metrics.json



This artifact provides class-specific evaluation information rather than relying only on aggregate accuracy.



This is particularly important because the evaluation dataset is imbalanced:



BENIGN     23

MALICIOUS   6



Accuracy alone therefore does not adequately describe malicious-class detection behavior.



## 12. ROC and Precision-Recall Evaluation



Score-based evaluation information is stored in:



ml/evaluation/results/roc\_pr\_data.json



The artifact contains ROC and precision-recall curve information where the evaluated model exposes a usable score or probability interface.



Non-finite threshold values produced by the underlying metric implementation are serialized as JSON-safe null values rather than invalid JSON numeric values.



## 13. Evaluation Metadata



The evaluation metadata is stored in:



ml/evaluation/results/evaluation\_metadata.json



The metadata records the evaluation configuration and provides traceability for the generated results.



The evaluation is tied to the frozen Phase 13 test-set contract and previously generated Phase 14/15 model artifacts.



## 14. Reproducibility



Phase 17 maintains the following reproducibility controls:



Frozen Phase 13 test data

Fixed feature contract

Fixed label mapping

Random state 42

Previously generated Phase 14 models

Previously generated Phase 15 models

Recorded model names

Recorded evaluation artifacts

Machine-readable result files

Evaluation metadata

Error-analysis artifacts

ROC/PR curve artifacts



The generated artifacts are intended to allow later phases to consume the evaluation results without retraining the models.



## 15. Dataset Limitations



The test dataset contains:



29 total samples

23 BENIGN

6 MALICIOUS



This is a very small evaluation population.



The results therefore cannot establish real-world generalization.



In particular:



A single missed malicious sample substantially changes recall.

A small number of false positives substantially changes precision.

ROC-AUC estimates are based on only 29 observations.

The controlled laboratory dataset does not represent the diversity of arbitrary browser extensions or production network environments.

Simulator timing does not represent production quantum hardware performance.



The results should therefore be treated as controlled experimental measurements.



## 16. Interpretation Constraints



Phase 17 does not make claims of:



Quantum advantage

Quantum supremacy

Production superiority

Guaranteed generalization

Universal model superiority

Guaranteed deployment performance



The measured results describe only the evaluated configurations on the frozen Phase 13 test set.



The observed Gradient Boosting and classical-model measurements should not be interpreted as a final production-model decision within this phase.



Likewise, the measured quantum-model results should not be interpreted as evidence that quantum machine learning is inherently ineffective or inherently advantageous.



## 17. Artifact Inventory



Phase 17 generated the following evaluation artifacts:



ml/evaluation/

â”œâ”€â”€ PHASE\_17\_DESIGN.md

â”œâ”€â”€ reports/

â”‚   â””â”€â”€ PHASE\_17\_MODEL\_EVALUATION\_REPORT.md

â”‚

â””â”€â”€ results/

&#x20;   â”œâ”€â”€ model\_evaluation.csv

&#x20;   â”œâ”€â”€ model\_evaluation.json

&#x20;   â”œâ”€â”€ confusion\_matrices.json

&#x20;   â”œâ”€â”€ per\_class\_metrics.json

&#x20;   â”œâ”€â”€ roc\_pr\_data.json

&#x20;   â”œâ”€â”€ error\_analysis.json

&#x20;   â””â”€â”€ evaluation\_metadata.json

## 18. Phase 18 Handoff



Phase 17 provides Phase 18 with:



Evaluated classical models

&#x20;       +

Evaluated quantum models

&#x20;       +

Confusion matrices

&#x20;       +

Per-class metrics

&#x20;       +

ROC/PR data

&#x20;       +

Error analysis

&#x20;       +

Inference characteristics

&#x20;       +

Evaluation metadata

&#x20;       â†“

Phase 18

Real-Time Detection Engine



Phase 18 can use these evaluation artifacts as the documented evidence base when implementing the real-time inference layer.



Any production-model selection or deployment decision must remain traceable to the formal evaluation and subsequent engineering requirements.



## 19. Phase 17 Completion Criteria



Phase 17 evaluation requirements:



&#x20;Phase 17 design documented.

&#x20;Frozen Phase 13 test contract verified.

&#x20;Six classical models evaluated.

&#x20;QSVC evaluated.

&#x20;VQC evaluated.

&#x20;Classification metrics generated.

&#x20;Confusion matrices generated.

&#x20;Per-class metrics generated.

&#x20;ROC/PR evaluation data generated.

&#x20;Error analysis generated.

&#x20;Inference characteristics recorded.

&#x20;Evaluation metadata generated.

&#x20;JSON artifacts validated.

&#x20;Automated Phase 17 tests pass.

&#x20;Phase 17 changes committed.

&#x20;Phase 17 changes pushed to GitHub.

&#x20;Git working tree clean.

&#x20;Phase 18 handoff verified.

## 20. Conclusion



Phase 17 successfully performed formal evaluation of the six classical models and two quantum models generated during Phases 14 and 15.



The evaluation used the frozen Phase 13 test set and preserved the established preprocessing, feature, label, and leakage-control contract.



The generated results include standard classification metrics, confusion matrices, per-class metrics, ROC/precision-recall data, error analysis, inference characteristics, and evaluation metadata.



The measurements demonstrate meaningful differences between the tested configurations, but the small controlled dataset limits the strength of any generalization conclusions.



Phase 17 therefore provides a reproducible evaluation evidence base for the next engineering stage without making unsupported claims about quantum advantage or declaring a final production model.



