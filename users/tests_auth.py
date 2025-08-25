from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.models import Organization
import json

BASE = "/api/v1"

class AuthApiTest(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(name="OrgA")
        self.user = get_user_model().objects.create_user(
            username="alice", password="1234", organization=self.org
        )

    def test_login_success_and_me(self):
        # login
        res = self.client.post(
            f"{BASE}/auth/login",
            data=json.dumps({"username": "alice", "password": "1234"}),
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 200, res.content)
        token = res.json()["access_token"]

        # /me with token
        res2 = self.client.get(
            f"{BASE}/auth/me",
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEqual(res2.status_code, 200, res2.content)
        data = res2.json()
        self.assertEqual(data["username"], "alice")
        self.assertEqual(data["organization_id"], self.org.id)

    def test_login_invalid_credentials(self):
        res = self.client.post(
            f"{BASE}/auth/login",
            data=json.dumps({"username": "alice", "password": "wrong"}),
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 401)

    def test_me_without_token_is_unauthorized(self):
        res = self.client.get(f"{BASE}/auth/me")
        self.assertEqual(res.status_code, 401)