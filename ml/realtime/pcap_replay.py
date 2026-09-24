from __future__ import annotations

import re
from pathlib import Path
from typing import Iterator

from scapy.all import Ether, IP, TCP
from scapy.utils import PcapNgReader

from ml.realtime.feature_adapter import adapt_observation


HTTP_METHOD_PATTERN = re.compile(rb"^(GET|POST)\s+\S+\s+HTTP/\d(?:\.\d)?\r?\n")
HTTP_RESPONSE_PATTERN = re.compile(rb"^HTTP/\d(?:\.\d)?\s+\d{3}\s")
JSON_PATTERN = re.compile(rb"^\s*[\{\[]")


def _payload(packet: Ether) -> bytes:
    """Return TCP application payload bytes."""
    if not packet.haslayer(TCP):
        return b""

    return bytes(packet[TCP].payload)


def _protocol_from_payload(payload: bytes) -> str:
    """Map packet application content to the Phase 13 protocol categories."""
    if not payload:
        return "TCP"

    if HTTP_METHOD_PATTERN.match(payload) or HTTP_RESPONSE_PATTERN.match(payload):
        return "HTTP"

    if JSON_PATTERN.match(payload):
        return "HTTP/JSON"

    return "TCP"


def _http_method_from_payload(payload: bytes) -> str | None:
    """Extract an HTTP request method when present."""
    match = HTTP_METHOD_PATTERN.match(payload)

    if match:
        return match.group(1).decode("ascii")

    return None


def packet_to_observation(
    packet: Ether,
    capture_start_time: float,
) -> dict[str, object]:
    """Convert one decoded PCAP packet into the Phase 13 raw feature contract."""
    packet_time = float(packet.time)

    observation = {
        "time_relative": packet_time - capture_start_time,
        "frame_len": len(bytes(packet)),
        "protocol": _protocol_from_payload(_payload(packet)),
        "http_method": _http_method_from_payload(_payload(packet)),
    }

    return adapt_observation(observation)


def iter_pcap_observations(
    pcap_path: str | Path,
) -> Iterator[dict[str, object]]:
    """Yield Phase 13-compatible observations from a PCAP/PCAPNG file."""
    path = Path(pcap_path)

    if not path.is_file():
        raise FileNotFoundError(f"PCAP file not found: {path}")

    reader = PcapNgReader(str(path))

    try:
        capture_start_time: float | None = None

        for raw_packet in reader:
            packet = Ether(bytes(raw_packet))

            if not packet.haslayer(IP):
                continue

            if capture_start_time is None:
                capture_start_time = float(packet.time)

            yield packet_to_observation(packet, capture_start_time)

    finally:
        reader.close()