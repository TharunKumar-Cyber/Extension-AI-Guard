from __future__ import annotations

from numbers import Real
from typing import Any


REQUIRED_FIELDS = (
    "time_relative",
    "frame_len",
    "protocol",
    "http_method",
)


def validate_observation(observation: dict[str, Any]) -> None:
    """Validate the raw traffic observation before preprocessing."""
    if not isinstance(observation, dict):
        raise TypeError("observation must be a dictionary")

    missing = [field for field in REQUIRED_FIELDS if field not in observation]
    if missing:
        raise ValueError(f"missing required fields: {missing}")

    for field in ("time_relative", "frame_len"):
        value = observation[field]

        if isinstance(value, bool) or not isinstance(value, Real):
            raise ValueError(f"{field} must be numeric")

        if not float(value) == float(value):
            raise ValueError(f"{field} must be finite")

        if abs(float(value)) == float("inf"):
            raise ValueError(f"{field} must be finite")

    protocol = observation["protocol"]
    if protocol not in {"HTTP", "HTTP/JSON", "TCP"}:
        raise ValueError(f"unsupported protocol: {protocol!r}")

    http_method = observation["http_method"]
    if http_method is not None and http_method not in {"GET", "POST"}:
        raise ValueError(f"unsupported http_method: {http_method!r}")


def adapt_observation(observation: dict[str, Any]) -> dict[str, Any]:
    """Validate and return the Phase 13-compatible raw feature mapping."""
    validate_observation(observation)

    return {
        "time_relative": float(observation["time_relative"]),
        "frame_len": float(observation["frame_len"]),
        "protocol": observation["protocol"],
        "http_method": observation["http_method"],
    }
