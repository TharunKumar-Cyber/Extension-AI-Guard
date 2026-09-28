import unittest
import uuid

from fastapi.testclient import TestClient

from backend.app.main import app


class TestAegisAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def create_authenticated_user(self):
        suffix = uuid.uuid4().hex[:10]

        user = {
            "username": f"phase19_aegis_test_{suffix}",
            "email": f"phase19_aegis_test_{suffix}@example.com",
            "password": "Phase19_TestPassword_123!",
        }

        response = self.client.post(
            "/api/auth/register",
            json=user,
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            "/api/auth/login",
            json={
                "email": user["email"],
                "password": user["password"],
            },
        )
        self.assertEqual(response.status_code, 200)

        token = response.json()["access_token"]

        return {
            "Authorization": f"Bearer {token}",
        }

    def test_welcome_endpoint(self):
        response = self.client.get("/api/aegis/welcome")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["assistant"], "Aegis")

    def test_status_requires_authentication(self):
        response = self.client.get("/api/aegis/status")

        self.assertEqual(response.status_code, 401)

    def test_status_with_authentication(self):
        headers = self.create_authenticated_user()

        response = self.client.get(
            "/api/aegis/status",
            headers=headers,
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertIn("user_id", data)
        self.assertIn("onboarding_exists", data)
        self.assertFalse(data["onboarding_exists"])

    def test_onboarding_lifecycle(self):
        headers = self.create_authenticated_user()

        response = self.client.post(
            "/api/aegis/onboarding/start",
            headers=headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["started"])
        self.assertFalse(response.json()["completed"])

        response = self.client.post(
            "/api/aegis/onboarding/step",
            headers=headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["current_step"], 2)

        response = self.client.post(
            "/api/aegis/onboarding/complete",
            headers=headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["completed"])

    def test_message_endpoint(self):
        headers = self.create_authenticated_user()

        response = self.client.post(
            "/api/aegis/message",
            headers=headers,
            json={
                "message": "How does Extension AI Guard detect malicious network traffic?"
            },
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["assistant"], "Aegis")
        self.assertIn("message", data)
        self.assertTrue(data["message"])

    def test_knowledge_endpoint(self):
        headers = self.create_authenticated_user()

        response = self.client.get(
            "/api/aegis/knowledge",
            headers=headers,
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["assistant"], "Aegis")
        self.assertIn("topics", data)
        self.assertGreater(len(data["topics"]), 0)

    def test_alert_explanation_endpoint(self):
        headers = self.create_authenticated_user()

        response = self.client.get(
            "/api/aegis/alerts/explain",
            headers=headers,
            params={
                "severity": "high",
                "title": "Malicious Network Request Detected",
                "message": (
                    "A suspicious network request was detected "
                    "from the browser extension."
                ),
            },
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["assistant"], "Aegis")
        self.assertEqual(data["severity"], "high")
        self.assertEqual(
            data["title"],
            "Malicious Network Request Detected",
        )
        self.assertIn("explanation", data)
        self.assertIn("recommended_action", data)


if __name__ == "__main__":
    unittest.main()
