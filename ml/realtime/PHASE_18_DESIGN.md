
@'
# Phase 18 — Real-Time Detection Engine

## 1. Phase Overview

Phase 18 converts the validated offline ML workflow into a controlled real-time detection pipeline for Extension AI Guard (EAG).

The engine will receive network-traffic observations, transform them into the same Phase 13 feature space, apply the selected detection model from the validated Phase 14/17 artifacts, and produce structured BENIGN/MALICIOUS detection results.

Phase 18 is an engineering phase. It does not retrain models or change the Phase 13 preprocessing contract.

## 2. Phase 18 Position

```text
Phase 13
Frozen Preprocessing
      ↓
Phase 14
Classical ML
      ↓
Phase 15
Quantum ML Research
      ↓
Phase 16
Model Comparison
      ↓
Phase 17
Model Evaluation
      ↓
Phase 18
Real-Time Detection Engine
      ↓
Phase 19
Backend API
````

## 3. Frozen Input Contract

The engine must preserve the Phase 13 feature contract:

1. `time_relative`
2. `frame_len`
3. `protocol_HTTP`
4. `protocol_HTTP_JSON`
5. `protocol_TCP`
6. `http_method_GET`
7. `http_method_POST`
8. `http_method_MISSING`

Labels remain:

```text
BENIGN = 0
MALICIOUS = 1
```

The Phase 13 preprocessing artifact must be reused.

Raw identifiers must not become model features:

* IP addresses
* Raw HTTP URI
* Frame numbers
* Capture-specific identifiers
* Other laboratory-specific identifiers

## 4. Detection Architecture

The initial real-time pipeline is:

```text
Network Traffic Observation
        ↓
Traffic Input
        ↓
Packet / Flow Feature Extraction
        ↓
Phase 13 Preprocessing
        ↓
Validated Feature Vector
        ↓
Detection Model
        ↓
Prediction + Score
        ↓
Detection Result
        ↓
Event / Log
```

The engine must keep feature extraction, preprocessing, inference, and result generation as separate responsibilities.

## 5. Model Policy

Phase 18 must consume an already-trained validated model.

It must not:

* Retrain models
* Modify the frozen test set
* Tune against the test set
* Change Phase 13 preprocessing
* Silently select a different feature space

The model configuration must be explicit and traceable.

The production-oriented inference path will initially use a validated classical model artifact because the Phase 15 quantum models were research experiments and their Phase 17 inference characteristics are simulator-specific.

Phase 18 must document the selected model and the reason for its use without making unsupported claims of universal superiority.

## 6. Input Modes

The initial engine will support controlled local inputs.

### Mode A — Single Observation

A single packet/traffic observation can be converted into the Phase 13 feature vector and evaluated.

### Mode B — Batch Stream

Multiple observations can be processed sequentially through the same inference pipeline.

### Mode C — PCAP Replay

Previously captured traffic may be replayed through the processing pipeline to validate real-time-style detection behavior without requiring live network traffic.

Live packet capture integration may be added only after the core inference engine is verified.

## 7. Detection Result Contract

Each detection event should contain:

* Event identifier
* Timestamp
* Prediction
* Prediction label
* Detection score where available
* Model name
* Feature schema version
* Processing status
* Input sequence information where applicable

Example conceptual result:

```json
{
  "event_id": "event-000001",
  "prediction": 1,
  "label": "MALICIOUS",
  "score": 0.91,
  "model": "gradient_boosting",
  "feature_schema": "phase13-v1",
  "status": "classified"
}
```

Example values are illustrative only.

## 8. Detection States

The engine will use explicit processing states:

```text
RECEIVED
    ↓
FEATURES_EXTRACTED
    ↓
PREPROCESSED
    ↓
CLASSIFIED
    ↓
RECORDED
```

Errors must be represented separately rather than silently converted into predictions.

## 9. Error Handling

The engine must safely handle:

* Missing input fields
* Invalid numeric values
* Unknown protocol values
* Missing HTTP method
* Feature-schema mismatch
* Missing model artifact
* Missing preprocessing artifact
* Model loading failure
* Prediction failure
* Invalid prediction output

Invalid input must not be silently treated as BENIGN.

## 10. Performance Measurements

Phase 18 will measure:

* Feature extraction time
* Preprocessing time
* Model inference time
* End-to-end processing time
* Events processed
* Successful classifications
* Failed classifications
* Throughput where measurable

Timing measurements are environment-specific and must not be presented as universal benchmarks.

## 11. Logging

The engine will produce structured logs suitable for later integration with:

* FastAPI
* Security Dashboard
* n8n
* Telegram alerting

Logging must avoid storing unnecessary sensitive network identifiers.

The Phase 18 engine should log detection events and operational errors separately.

## 12. Testing Requirements

Automated tests must verify:

* Phase 13 preprocessing artifact loads.
* Required feature schema is preserved.
* Valid observations are transformed correctly.
* Missing HTTP method is represented correctly.
* Model artifact loads successfully.
* Single observations can be classified.
* Batch observations can be classified.
* Detection results follow the defined schema.
* Invalid input is rejected safely.
* Model loading failures are handled.
* Prediction failures are handled.
* No raw leakage fields enter the model feature vector.
* End-to-end inference completes successfully.

## 13. Security Requirements

The engine must:

* Validate input before inference.
* Avoid trusting externally supplied prediction labels.
* Avoid arbitrary file loading.
* Avoid arbitrary model paths from untrusted input.
* Avoid executing network-provided code.
* Keep model and preprocessing paths controlled by configuration.
* Prevent malformed observations from crashing the entire processing loop.
* Avoid logging unnecessary sensitive traffic information.

## 14. Proposed Directory Structure

```text
ml/
└── realtime/
    ├── README.md
    ├── realtime_config.py
    ├── feature_adapter.py
    ├── detection_engine.py
    ├── detection_result.py
    ├── replay.py
    ├── benchmark.py
    ├── test_realtime.py
    │
    ├── artifacts/
    │
    └── results/
        ├── detection_events.jsonl
        ├── realtime_metrics.json
        └── benchmark_results.json
```

The implementation directory will be populated incrementally after the design is committed.

## 15. Phase 18 Experiments

### Experiment A — Single Observation Inference

Verify that a controlled feature observation can pass through preprocessing and model inference.

### Experiment B — Batch Stream Inference

Process multiple observations sequentially and verify event ordering and result integrity.

### Experiment C — PCAP Replay

Replay processed traffic observations through the detection pipeline and record detection events.

### Experiment D — Performance Measurement

Measure feature-processing, inference, and end-to-end latency under controlled local execution.

## 16. Reproducibility

The engine must record:

* Phase 18 version
* Model name
* Model artifact path
* Preprocessor artifact path
* Feature schema
* Python version
* Package versions
* Timestamp
* Input mode
* Number of processed observations
* Successful classifications
* Failed classifications

## 17. Phase 19 Handoff

Phase 18 will provide Phase 19 with:

```text
Real-Time Detection Engine
        ↓
Stable Detection Result Contract
        ↓
Structured Detection Events
        ↓
Performance Metrics
        ↓
Error Handling
        ↓
FastAPI Integration
```

Phase 19 will expose the detection capabilities through the backend API.

## 18. Phase 18 Completion Criteria

Phase 18 is complete only when:

* [ ] Phase 18 design is committed.
* [ ] Phase 13 preprocessing artifact is reused.
* [ ] Validated model artifact is loaded.
* [ ] Feature adapter is implemented.
* [ ] Single-observation inference works.
* [ ] Batch processing works.
* [ ] PCAP replay works.
* [ ] Detection result schema is implemented.
* [ ] Error handling is tested.
* [ ] Security validation is tested.
* [ ] Performance measurements are generated.
* [ ] Automated tests pass.
* [ ] Phase 18 documentation is complete.
* [ ] Phase 19 handoff is documented.
* [ ] Git working tree is clean.
* [ ] Phase 18 changes are committed and pushed.

## 19. Research and Deployment Boundary

Phase 18 does not claim that the current laboratory model is production-ready.

The current dataset remains small and controlled.

The engine therefore establishes the real-time inference architecture and controlled operational behavior. Broader validation, deployment hardening, live HTTPS/TLS traffic support, and enterprise-scale operation are separate engineering concerns.

## 20. Conclusion

Phase 18 establishes the real-time detection layer of Extension AI Guard while preserving the validated Phase 13 feature contract and the evaluated model artifacts from earlier phases.

The implementation will proceed incrementally so that every transformation, prediction, event, error, and performance measurement remains testable and traceable before the system is handed to Phase 19.
