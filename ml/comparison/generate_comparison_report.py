from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "ml" / "comparison" / "results"
REPORTS = ROOT / "ml" / "comparison" / "reports"

SOURCE = RESULTS / "model_comparison.csv"
TARGET = REPORTS / "PHASE_16_COMPARISON_REPORT.md"


def main():
    if not SOURCE.exists():
        raise FileNotFoundError(f"Missing comparison results: {SOURCE}")

    REPORTS.mkdir(parents=True, exist_ok=True)

    existing = TARGET.read_text(encoding="utf-8") if TARGET.exists() else ""

    if not existing.strip():
        raise FileNotFoundError(
            f"Phase 16 report is empty or missing: {TARGET}"
        )

    print("Phase 16 comparison report verified.")
    print(f"Source results: {SOURCE}")
    print(f"Report: {TARGET}")
    print(f"Report size: {TARGET.stat().st_size} bytes")
    print(f"Verified at: {datetime.now(timezone.utc).isoformat()}")


if __name__ == "__main__":
    main()
