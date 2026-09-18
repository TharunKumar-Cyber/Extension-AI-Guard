import csv
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path.home() / "eag-processing"
OUTPUT_FILE = BASE_DIR / "packet_features.csv"

FIELDS = [
    "frame.number",
    "frame.time_relative",
    "ip.src",
    "ip.dst",
    "tcp.srcport",
    "tcp.dstport",
    "frame.len",
    "_ws.col.Protocol",
    "http.request.method",
    "http.request.uri",
]


def extract_packets(capture_file):
    command = [
        "tshark",
        "-r",
        str(capture_file),
        "-T",
        "fields",
    ]

    for field in FIELDS:
        command.extend(["-e", field])

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=True,
    )

    return result.stdout.splitlines()


def parse_packets(lines):
    packets = []

    for line in lines:
        values = line.split("\t")

        if len(values) != len(FIELDS):
            values.extend([""] * (len(FIELDS) - len(values)))

        packet = dict(zip(FIELDS, values))
        packets.append(packet)

    return packets


def save_csv(packets):
    fieldnames = [
        "frame_number",
        "time_relative",
        "src_ip",
        "dst_ip",
        "src_port",
        "dst_port",
        "packet_length",
        "protocol",
        "http_method",
        "http_uri",
    ]

    with open(OUTPUT_FILE, "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for packet in packets:
            writer.writerow(
                {
                    "frame_number": packet.get("frame.number", ""),
                    "time_relative": packet.get("frame.time_relative", ""),
                    "src_ip": packet.get("ip.src", ""),
                    "dst_ip": packet.get("ip.dst", ""),
                    "src_port": packet.get("tcp.srcport", ""),
                    "dst_port": packet.get("tcp.dstport", ""),
                    "packet_length": packet.get("frame.len", ""),
                    "protocol": packet.get("_ws.col.Protocol", ""),
                    "http_method": packet.get("http.request.method", ""),
                    "http_uri": packet.get("http.request.uri", ""),
                }
            )


def main():
    if len(sys.argv) != 2:
        raise SystemExit(
            "Usage: python3 packet_processor.py <capture.pcapng>"
        )

    capture_file = Path(sys.argv[1]).expanduser()

    if not capture_file.is_absolute():
        capture_file = BASE_DIR / capture_file

    if not capture_file.exists():
        raise FileNotFoundError(
            f"Capture file not found: {capture_file}"
        )

    lines = extract_packets(capture_file)
    packets = parse_packets(lines)
    save_csv(packets)

    print(f"Processed packets: {len(packets)}")
    print(f"Input file: {capture_file}")
    print(f"Output file: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
