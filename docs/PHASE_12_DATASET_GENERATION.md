# Phase 12 — Dataset Generation

## 1. Objective

The objective of Phase 12 is to generate and validate a labeled packet-level
dataset for Extension AI Guard (EAG).

The dataset contains controlled BENIGN and MALICIOUS browser-extension traffic
captured in the project test environment.

The dataset is intended for subsequent preprocessing and machine-learning
experiments in Phases 13–17.

The controlled malicious extension is used only as a safe test-data source.
The final EAG system is intended to analyze network traffic from extensions
being tested, including previously unseen extensions.

---

## 2. Dataset Generation Environment

Operating system:
- Parrot OS

Network:
- Windows host: 192.168.31.54
- Parrot test environment: 192.168.31.9
- Test server port: 9000

Traffic protocol:
- Controlled HTTP traffic over TCP

Packet capture / inspection:
- TShark / Wireshark tooling

---

## 3. BENIGN Dataset Generation

Four validated BENIGN packet captures were generated:

| Capture | Packets | HTTP Requests | Expected Traffic |
|---|---:|---:|---|
| benign_01.pcapng | 64 | 5 | GET /safe |
| benign_02.pcapng | 12 | 1 | GET /safe |
| benign_03.pcapng | 24 | 2 | GET /safe |
| benign_04.pcapng | 12 | 1 | GET /safe |
| **Total** | **112** | **9** | **BENIGN** |

Each capture was inspected using TShark.

No BENIGN capture used in the final dataset contained the controlled
`/malicious-test` endpoint.

---

## 4. MALICIOUS Dataset Generation

The controlled malicious-extension traffic was captured and labeled as
MALICIOUS.

Source artifact:

`malicious_01_labeled.tsv`

Packet records:

- 32 MALICIOUS packets

The traffic includes controlled requests to:

`/malicious-test`

The malicious traffic is a local/LAN simulation used for cybersecurity
research and dataset generation.

---

## 5. Packet-Level Dataset

The final master dataset contains packet-level network observations.

Schema:

1. frame_number
2. time_relative
3. ip_src
4. ip_dst
5. tcp_srcport
6. tcp_dstport
7. frame_len
8. protocol
9. http_method
10. http_uri
11. label

Labels:

- BENIGN
- MALICIOUS

---

## 6. Final Dataset Composition

Final dataset:

`dataset/dataset_final.tsv`

Frozen Phase 12 copy:

`dataset/dataset_final_phase12.tsv`

Dataset size:

- Total samples: 144
- BENIGN: 112
- MALICIOUS: 32

Class distribution:

- BENIGN: 77.78%
- MALICIOUS: 22.22%

The class distribution is retained as generated. Class balancing, if required
for model training, will be addressed during later preprocessing/model
development rather than altering the original Phase 12 dataset.

---

## 7. Packet Size Statistics

Overall:

- Total packets: 144
- Total bytes: 33,924
- Average packet size: 235.58 bytes

BENIGN:

- Packets: 112
- Average packet size: 93.96 bytes
- Minimum packet size: 54 bytes
- Maximum packet size: 342 bytes

MALICIOUS:

- Packets: 32
- Average packet size: 731.25 bytes
- Minimum packet size: 54 bytes
- Maximum packet size: 10,169 bytes

Packet size is one of the network characteristics available to later machine
learning experiments. It is not treated as the sole classification criterion.

---

## 8. Feature Engineering Artifacts

The following per-capture artifacts were generated:

- benign_01_features.csv
- benign_01_engineered.csv
- benign_02_features.csv
- benign_02_engineered.csv
- benign_03_features.csv
- benign_03_engineered.csv
- benign_04_features.csv
- benign_04_engineered.csv

The engineered traffic summaries include characteristics such as:

- total packet count
- total bytes
- average packet size
- minimum packet size
- maximum packet size
- traffic duration
- packets per second
- bytes per second
- HTTP request count
- HTTP POST count

These features provide the foundation for later ML processing.

---

## 9. Dataset Quality Validation

The final dataset was checked for structural and data-quality problems.

### Schema validation

All 144 data records contain 11 fields.

Result: PASS

### Duplicate validation

Duplicate packet records detected:

0

Result: PASS

### Packet-size validation

All packet-size values were present and numeric.

Result: PASS

### Label validation

All records use one of the two expected labels:

- BENIGN
- MALICIOUS

Result: PASS

### BENIGN malicious-traffic leakage check

The final dataset was checked for `/malicious-test` appearing in BENIGN
records.

Result:

No BENIGN record contained `/malicious-test`.

Result: PASS

### HTTP behavior validation

Observed labeled HTTP traffic:

- GET `/safe` → BENIGN
- POST `/malicious-test` → MALICIOUS

Result: PASS

---

## 10. Invalid Capture Handling

During dataset generation, earlier captures were identified as invalid because
they contained traffic inconsistent with their intended BENIGN label.

These captures were preserved separately for evidence and were not included
in the final master dataset.

Examples:

- safe_01_invalid_malicious_test.pcapng
- benign_01_invalid_malicious_active.pcapng

This prevents known noisy/incorrect samples from contaminating the final
Phase 12 dataset.

---

## 11. Dataset Integrity

SHA-256 hash of the final dataset:

`3570dce2ef318eb2500389d78964d6221c0569ca2a72a22509e274ba7b2d9379`

The frozen Phase 12 copy was independently hashed and produced the same
SHA-256 value.

Therefore:

`dataset_final.tsv`

and

`dataset_final_phase12.tsv`

are byte-for-byte identical at the time of freezing.

---

## 12. Phase 12 Output

The primary Phase 12 output is:

`dataset/dataset_final.tsv`

Frozen copy:

`dataset/dataset_final_phase12.tsv`

Supporting packet and feature artifacts are stored under:

`dataset/`

These artifacts will be used by Phase 13 for dataset preprocessing.

---

## 13. Relationship to the EAG Pipeline

Phase 12 establishes the dataset stage of the EAG pipeline:

Browser Extension
        ↓
Network Traffic
        ↓
Packet Capture
        ↓
Packet Processing
        ↓
Feature Engineering
        ↓
Phase 12 Dataset
        ↓
Phase 13 Preprocessing
        ↓
Phase 14 Classical ML
        ↓
Phase 15 Quantum ML Research
        ↓
Phase 16 Model Comparison
        ↓
Phase 17 Evaluation
        ↓
Phase 18 Real-Time Detection

The final system is intended to use learned traffic characteristics to classify
traffic associated with browser extensions as BENIGN or MALICIOUS.

---

## 14. Phase 12 Verification Summary

| Validation | Result |
|---|---|
| BENIGN packet generation | PASS |
| MALICIOUS packet generation | PASS |
| Packet extraction | PASS |
| Label generation | PASS |
| Dataset combination | PASS |
| Schema validation | PASS |
| Duplicate check | PASS |
| Invalid-value check | PASS |
| Packet-size analysis | PASS |
| Malicious URI leakage check | PASS |
| Final statistics | PASS |
| SHA-256 integrity verification | PASS |
| Frozen dataset copy | PASS |

## Phase Status

Phase 12 — Dataset Generation

Implementation/Data Generation: COMPLETE

Final documentation: COMPLETE

GitHub synchronization: Pending

Phase 13: Not started
