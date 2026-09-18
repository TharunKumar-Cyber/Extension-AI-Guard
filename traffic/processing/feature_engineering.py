import csv
from pathlib import Path


INPUT_FILE = Path.home() / "eag-processing" / "packet_features.csv"
OUTPUT_FILE = Path.home() / "eag-processing" / "engineered_features.csv"


def load_packets():
    with open(INPUT_FILE, newline="") as csv_file:
        return list(csv.DictReader(csv_file))


def calculate_features(packets):
    if not packets:
        raise ValueError("No packets found in input CSV.")

    packet_lengths = [
        int(packet["packet_length"])
        for packet in packets
        if packet["packet_length"]
    ]

    times = [
        float(packet["time_relative"])
        for packet in packets
        if packet["time_relative"]
    ]

    request_packets = [
        packet
        for packet in packets
        if packet["http_method"]
    ]

    post_count = sum(
        1
        for packet in request_packets
        if packet["http_method"].upper() == "POST"
    )

    total_bytes = sum(packet_lengths)
    total_packets = len(packets)

    duration = max(times) - min(times) if times else 0.0

    packets_per_second = (
        total_packets / duration
        if duration > 0
        else 0.0
    )

    bytes_per_second = (
        total_bytes / duration
        if duration > 0
        else 0.0
    )

    return {
        "total_packets": total_packets,
        "total_bytes": total_bytes,
        "average_packet_size": sum(packet_lengths) / len(packet_lengths),
        "minimum_packet_size": min(packet_lengths),
        "maximum_packet_size": max(packet_lengths),
        "traffic_duration_seconds": duration,
        "packets_per_second": packets_per_second,
        "bytes_per_second": bytes_per_second,
        "http_request_count": len(request_packets),
        "http_post_count": post_count,
    }


def save_features(features):
    with open(OUTPUT_FILE, "w", newline="") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=features.keys(),
        )

        writer.writeheader()
        writer.writerow(features)


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Input file not found: {INPUT_FILE}"
        )

    packets = load_packets()
    features = calculate_features(packets)
    save_features(features)

    print("Feature engineering completed.")
    print(f"Processed packets: {len(packets)}")
    print(f"Output file: {OUTPUT_FILE}")

    for name, value in features.items():
        print(f"{name}: {value}")


if __name__ == "__main__":
    main()
