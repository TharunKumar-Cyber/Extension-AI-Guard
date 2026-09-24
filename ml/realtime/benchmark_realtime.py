from __future__ import annotations

import json
import time
from pathlib import Path

from ml.realtime.detection_engine import DetectionEngine


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RESULTS_DIR = PROJECT_ROOT / "ml" / "realtime" / "results"
BENCHMARK_PATH = RESULTS_DIR / "phase18_benchmark.json"

BENCHMARK_SAMPLES = 50

SAMPLE_OBSERVATION = {
    "time_relative": 1.25,
    "frame_len": 512,
    "protocol": "TCP",
    "http_method": None,
}


def run_benchmark(
    samples: int = BENCHMARK_SAMPLES,
) -> dict[str, float | int]:
    """Measure Phase 18 real-time detection throughput and latency."""
    if samples <= 0:
        raise ValueError("samples must be greater than zero")

    engine = DetectionEngine()

    durations: list[float] = []
    errors = 0

    wall_start = time.perf_counter()

    for _ in range(samples):
        start = time.perf_counter()
        result = engine.detect(SAMPLE_OBSERVATION)
        duration = time.perf_counter() - start

        durations.append(duration)

        if result.status != "CLASSIFIED":
            errors += 1

    wall_time = time.perf_counter() - wall_start

    average_detection = sum(durations) / len(durations)
    throughput = samples / wall_time

    return {
        "samples": samples,
        "wall_time_seconds": wall_time,
        "throughput_per_second": throughput,
        "avg_detection_ms": average_detection * 1000,
        "min_detection_ms": min(durations) * 1000,
        "max_detection_ms": max(durations) * 1000,
        "errors": errors,
    }


def save_benchmark_result(
    result: dict[str, float | int],
) -> Path:
    """Save benchmark results as JSON."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    with BENCHMARK_PATH.open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2)

    return BENCHMARK_PATH


if __name__ == "__main__":
    benchmark_result = run_benchmark()
    output_path = save_benchmark_result(benchmark_result)

    print(json.dumps(benchmark_result, indent=2))
    print(f"result_file={output_path}")