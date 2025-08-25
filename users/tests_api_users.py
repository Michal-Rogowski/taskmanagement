from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import Organization
import json

BASE = "/api/v1"


def login(client, username, password):
    res = client.post(
        f"{BASE}/auth/login",
        data=json.dumps({"username": username, "password": password}),
        content_type="application/json",
    )
    assert res.status_code == 200, res.content
    return res.json()["access_token"]


class UsersApiTest(TestCase):
    def setUp(self):
        self.orgA = Organization.objects.create(name="OrgA")
        self.orgB = Organization.objects.create(name="OrgB")
        User = get_user_model()
        self.alice = User.objects.create_user(
            username="alice", password="1234", organization=self.orgA
        )
        self.bob = User.objects.create_user(
            username="bob", password="1234", organization=self.orgA
        )
        User.objects.create_user(
            username="charlie", password="1234", organization=self.orgB
        )
        self.token_alice = login(self.client, "alice", "1234")

    def test_list_users_requires_auth_and_scopes(self):
        res = self.client.get(f"{BASE}/users/")
        self.assertEqual(res.status_code, 401)

        res = self.client.get(
            f"{BASE}/users/",
            HTTP_AUTHORIZATION=f"Bearer {self.token_alice}",
        )
        self.assertEqual(res.status_code, 200)
        usernames = [u["username"] for u in res.json()]
        self.assertCountEqual(usernames, ["alice", "bob"])

    def test_create_user_requires_auth(self):
        res = self.client.post(
            f"{BASE}/users/",
            data=json.dumps({"username": "dave", "password": "1234"}),
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 401)

        res = self.client.post(
            f"{BASE}/users/",
            data=json.dumps({"username": "dave", "password": "1234"}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.token_alice}",
        )
        self.assertEqual(res.status_code, 201, res.content)
        self.assertTrue(
            get_user_model()
            .objects.filter(username="dave", organization=self.orgA)
            .exists()
        )

