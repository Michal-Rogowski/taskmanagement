from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import Organization
from tasks.models import Task
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

class TasksApiMultiTenancyTest(TestCase):
    def setUp(self):
        # Orgs & users
        self.orgA = Organization.objects.create(name="OrgA")
        self.orgB = Organization.objects.create(name="OrgB")
        User = get_user_model()
        self.alice = User.objects.create_user(username="alice", password="1234", organization=self.orgA)
        self.bob   = User.objects.create_user(username="bob",   password="1234", organization=self.orgB)

        # Tasks per org
        Task.all_objects.create(title="A1", organization=self.orgA, assigned_to=self.alice, metadata={"sprint": 21, "priority": 5})
        Task.all_objects.create(title="A2", organization=self.orgA, assigned_to=self.alice, metadata={"sprint": 22, "priority": 2})
        Task.all_objects.create(title="B1", organization=self.orgB, assigned_to=self.bob,   metadata={"sprint": 7,  "priority": 1})

        # Tokens
        self.token_alice = login(self.client, "alice", "1234")
        self.token_bob   = login(self.client, "bob",   "1234")

    def test_tasks_are_scoped_to_authenticated_users_org(self):
        # Alice sees only A*
        res = self.client.get(
            f"{BASE}/tasks/?page=1&page_size=50",
            HTTP_AUTHORIZATION=f"Bearer {self.token_alice}",
        )
        self.assertEqual(res.status_code, 200, res.content)
        titles = [item["title"] for item in res.json()["items"]]
        self.assertCountEqual(titles, ["A1", "A2"])

        # Bob sees only B*
        res2 = self.client.get(
            f"{BASE}/tasks/?page=1&page_size=50",
            HTTP_AUTHORIZATION=f"Bearer {self.token_bob}",
        )
        self.assertEqual(res2.status_code, 200, res2.content)
        titles2 = [item["title"] for item in res2.json()["items"]]
        self.assertCountEqual(titles2, ["B1"])

    def test_metadata_filters_with_token(self):
        # Alice + sprint filter
        res = self.client.get(
            f"{BASE}/tasks/?metadata[sprint]=21",
            HTTP_AUTHORIZATION=f"Bearer {self.token_alice}",
        )
        self.assertEqual(res.status_code, 200)
        items = res.json()["items"]
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["title"], "A1")

    def test_list_requires_authentication(self):
        res = self.client.get(f"{BASE}/tasks/")
        self.assertEqual(res.status_code, 401)
