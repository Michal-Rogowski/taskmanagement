from django.test import TestCase, SimpleTestCase
from django.core.management import call_command
from io import StringIO
from users.models import Organization, User
from .models import Task
from django.core.exceptions import ValidationError
from core.tenant import set_org
from .schemas import TaskIn


class TaskModelTest(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(name="TestOrg")
        self.user = User.objects.create_user(username="alice", password="1234", organization=self.org)
        set_org(self.org.id)

    def test_create_and_query_tasks(self):
        Task.all_objects.create(title="Fix bug", organization=self.org, metadata={"sprint": 21})
        Task.all_objects.create(title="Write docs", organization=self.org, metadata={"sprint": 22})
        sprint21_tasks = Task.objects.filter(metadata__sprint=21)
        self.assertEqual(sprint21_tasks.count(), 1)
        self.assertEqual(sprint21_tasks.first().title, "Fix bug")

    def test_org_isolation(self):
        other = Organization.objects.create(name="OtherOrg")
        bob = User.objects.create_user(username="bob", password="x", organization=other)
        Task.all_objects.create(title="A1", organization=self.org, metadata={"tag": "x"})
        Task.all_objects.create(title="B1", organization=other, assigned_to=bob, metadata={"tag": "y"})
        self.assertEqual(Task.all_objects.filter(organization=self.org).count(), 1)
        self.assertEqual(Task.all_objects.filter(organization=other).count(), 1)

    def test_cannot_assign_user_from_other_org(self):
        other = Organization.objects.create(name="Other")
        bob = User.objects.create_user(username="bob", password="x", organization=other)
        with self.assertRaises(ValidationError):
            Task.objects.create(title="Bad assign", organization=self.org, assigned_to=bob)

    def tearDown(self):
        set_org(None)


class FindTasksCommandTest(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(name="TestOrg")
        self.user = User.objects.create_user(username="alice", password="1234", organization=self.org)

    def test_find_tasks_command_runs(self):
        Task.all_objects.create(title="A1", organization=self.org, metadata={"tag": "x", "priority": 3})
        out = StringIO()
        call_command("find_tasks", "--org", "TestOrg", "--meta", "priority__gt=2", stdout=out)
        self.assertIn("A1", out.getvalue())


class TaskSchemaDefaultTest(SimpleTestCase):
    def test_taskin_metadata_default_is_unique(self):
        t1 = TaskIn(title="One")
        t2 = TaskIn(title="Two")
        t1.metadata["a"] = 1
        self.assertEqual(t2.metadata, {})
