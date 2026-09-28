import unittest
from datetime import datetime, timezone

from backend.app.models.network_request import NetworkRequest
from backend.app.services.alert import create_alert
from backend.app.services.detection import analyze_request
from backend.app.services.security_event import create_security_event


class TestDetectionPipeline(unittest.TestCase):

    def make_request(self, domain="example.com"):
        return NetworkRequest(
            request_id="test-001",
            url=f"https://{domain}/",
            method="GET",
            domain=domain,
            timestamp=datetime.now(timezone.utc),
        )

    def test_benign_domain(self):
        result = analyze_request(self.make_request("example.com"))

        self.assertFalse(result.is_malicious)
        self.assertEqual(result.confidence, 0.10)
        self.assertEqual(result.threat_type, "none")
        self.assertEqual(result.request_id, "test-001")

    def test_malicious_domain(self):
        result = analyze_request(self.make_request("malware.test"))

        self.assertTrue(result.is_malicious)
        self.assertEqual(result.confidence, 0.95)
        self.assertEqual(result.threat_type, "suspicious_domain")
        self.assertEqual(result.result_id, "det-test-001")

    def test_suspicious_domain_is_case_insensitive(self):
        result = analyze_request(self.make_request("MALWARE.TEST"))

        self.assertTrue(result.is_malicious)
        self.assertEqual(result.threat_type, "suspicious_domain")

    def test_benign_result_creates_no_alert(self):
        result = analyze_request(self.make_request("example.com"))

        alert = create_alert(result)

        self.assertIsNone(alert)

    def test_malicious_result_creates_high_alert(self):
        result = analyze_request(self.make_request("malware.test"))

        alert = create_alert(result)

        self.assertIsNotNone(alert)
        self.assertEqual(alert.alert_id, "alert-det-test-001")
        self.assertEqual(alert.result_id, "det-test-001")
        self.assertEqual(alert.severity, "high")
        self.assertEqual(
            alert.title,
            "Malicious Network Request Detected",
        )
        self.assertEqual(alert.message, result.explanation)

    def test_security_event_creation(self):
        event = create_security_event(
            event_type="network_request",
            source="extension",
            severity="high",
            description="Test malicious event",
        )

        self.assertEqual(event.event_type, "network_request")
        self.assertEqual(event.source, "extension")
        self.assertEqual(event.severity, "high")
        self.assertEqual(event.description, "Test malicious event")
        self.assertTrue(event.event_id.startswith("event-"))
        self.assertIsNotNone(event.timestamp)


if __name__ == "__main__":
    unittest.main()
