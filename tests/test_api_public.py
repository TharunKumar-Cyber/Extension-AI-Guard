import unittest
from datetime import datetime, timezone

from fastapi.testclient import TestClient

from backend.app.main import app


class TestPublicAndNetworkAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_root_endpoint(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["project"], "Extension AI Guard")
        self.assertEqual(data["status"], "running")
        self.assertIn("version", data)

    def test_health_endpoint(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "healthy")

    def test_api_status_endpoint(self):
        response = self.client.get("/api/status")

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["status"], "online")
        self.assertEqual(data["service"], "Extension AI Guard API")

    def test_database_status_endpoint(self):
        response = self.client.get("/api/database-status")

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), dict)

    def test_network_request_benign(self):
        payload = {
            "request_id": "api-test-benign",
            "url": "https://example.com/",
            "method": "GET",
            "domain": "example.com",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        response = self.client.post(
            "/api/network-requests",
            json=payload,
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["status"], "analyzed")
        self.assertFalse(data["detection"]["is_malicious"])
        self.assertEqual(data["detection"]["confidence"], 0.10)
        self.assertEqual(data["detection"]["threat_type"], "none")
        self.assertIsNone(data["alert"])
        self.assertEqual(
            data["security_event"]["severity"],
            "low",
        )

    def test_network_request_malicious(self):
        payload = {
            "request_id": "api-test-malicious",
            "url": "https://malware.test/",
            "method": "GET",
            "domain": "malware.test",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        response = self.client.post(
            "/api/network-requests",
            json=payload,
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["status"], "analyzed")
        self.assertTrue(data["detection"]["is_malicious"])
        self.assertEqual(data["detection"]["confidence"], 0.95)
        self.assertEqual(
            data["detection"]["threat_type"],
            "suspicious_domain",
        )

        self.assertIsNotNone(data["alert"])
        self.assertEqual(data["alert"]["severity"], "high")

        self.assertEqual(
            data["security_event"]["severity"],
            "high",
        )

    def test_network_request_rejects_invalid_method(self):
        payload = {
            "request_id": "api-test-invalid",
            "url": "https://example.com/",
            "method": "INVALID",
            "domain": "example.com",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        response = self.client.post(
            "/api/network-requests",
            json=payload,
        )

        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
