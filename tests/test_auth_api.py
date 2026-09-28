import unittest
import uuid

from fastapi.testclient import TestClient

from backend.app.main import app


class TestAuthenticationAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def unique_user(self):
        suffix = uuid.uuid4().hex[:10]

        return {
            "username": f"phase19_{suffix}",
            "email": f"phase19_{suffix}@example.com",
            "password": "Phase19_TestPassword_123!",
        }

    def test_register_user(self):
        user = self.unique_user()

        response = self.client.post(
            "/api/auth/register",
            json=user,
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["status"], "registered")
        self.assertEqual(data["user"]["username"], user["username"])
        self.assertEqual(data["user"]["email"], user["email"])
        self.assertTrue(data["user"]["is_active"])
        self.assertIn("id", data["user"])

    def test_login_returns_jwt(self):
        user = self.unique_user()

        register_response = self.client.post(
            "/api/auth/register",
            json=user,
        )

        self.assertEqual(register_response.status_code, 200)

        response = self.client.post(
            "/api/auth/login",
            json={
                "email": user["email"],
                "password": user["password"],
            },
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["status"], "authenticated")
        self.assertIsInstance(data["access_token"], str)
        self.assertGreater(len(data["access_token"]), 20)
        self.assertEqual(data["user"]["email"], user["email"])

    def test_login_rejects_wrong_password(self):
        user = self.unique_user()

        register_response = self.client.post(
            "/api/auth/register",
            json=user,
        )

        self.assertEqual(register_response.status_code, 200)

        response = self.client.post(
            "/api/auth/login",
            json={
                "email": user["email"],
                "password": "WrongPassword_123!",
            },
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["status"], "failed")
        self.assertEqual(
            data["message"],
            "Invalid email or password",
        )

    def test_login_rejects_unknown_email(self):
        response = self.client.post(
            "/api/auth/login",
            json={
                "email": f"unknown_{uuid.uuid4().hex}@example.com",
                "password": "Phase19_TestPassword_123!",
            },
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["status"], "failed")
        self.assertEqual(
            data["message"],
            "Invalid email or password",
        )

    def test_duplicate_email_is_rejected(self):
        user = self.unique_user()

        first_response = self.client.post(
            "/api/auth/register",
            json=user,
        )

        self.assertEqual(first_response.status_code, 200)

        duplicate_user = {
            **user,
            "username": f"another_{uuid.uuid4().hex[:10]}",
        }

        response = self.client.post(
            "/api/auth/register",
            json=duplicate_user,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["detail"],
            "Email or username already registered",
        )

    def test_duplicate_username_is_rejected(self):
        user = self.unique_user()

        first_response = self.client.post(
            "/api/auth/register",
            json=user,
        )

        self.assertEqual(first_response.status_code, 200)

        duplicate_user = {
            **user,
            "email": f"another_{uuid.uuid4().hex}@example.com",
        }

        response = self.client.post(
            "/api/auth/register",
            json=duplicate_user,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["detail"],
            "Email or username already registered",
        )


if __name__ == "__main__":
    unittest.main()
