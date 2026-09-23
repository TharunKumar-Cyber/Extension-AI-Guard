# Phase 17 — Model Evaluation

## Purpose

Phase 17 formally evaluates the existing Phase 14 classical ML models and Phase 15 quantum ML models using the frozen Phase 13 test set.

No model retraining or test-set tuning is permitted.

## Evaluation Contract

- Test samples: 29
- BENIGN: 23
- MALICIOUS: 6
- Features: 8
- Random state: 42
- BENIGN = 0
- MALICIOUS = 1

## Evaluation Scope

Phase 17 evaluates:

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC
- Confusion matrices
- True positives
- True negatives
- False positives
- False negatives
- Per-class performance
- ROC behavior where supported
- Precision-recall behavior where supported
- Prediction probabilities or decision scores where available
- Inference characteristics
- Error analysis
- Reproducibility

## Models

Classical:
- Logistic Regression
- Decision Tree
- Random Forest
- SVM
- KNN
- Gradient Boosting

Quantum:
- QSVC
- VQC

## Dataset Limitation

The test set contains only 29 samples, including six MALICIOUS samples. Therefore individual errors can substantially change recall and other metrics.

Results must not be interpreted as proof of production-level generalization.

## Security and Leakage Controls

Phase 13 leakage controls remain mandatory.

Raw IP addresses, raw HTTP URIs, frame numbers, and capture-specific identifiers must not become model features.

## No Unsupported Claims

Phase 17 must not claim:
- Quantum advantage
- Quantum supremacy
- Guaranteed production accuracy
- Guaranteed real-world generalization
- Universal model superiority

## Phase 18 Handoff

Phase 17 provides validated evaluation results, error analysis, confidence/score information, and inference characteristics to Phase 18 Real-Time Detection Engine.

## Completion Criteria

- Evaluation implementation complete
- Confusion matrices generated
- Per-class metrics generated
- ROC/PR evaluation generated where supported
- Error analysis generated
- Metadata generated
- Automated tests pass
- Evaluation report generated
- Phase 18 handoff documented
- Git commit and push completed
- Working tree clean
