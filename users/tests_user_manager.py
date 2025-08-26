from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import Organization
from core.tenant import set_org


class UserManagerTest(TestCase):
    def setUp(self):
        self.orgA = Organization.objects.create(name="OrgA")
        self.orgB = Organization.objects.create(name="OrgB")
        User = get_user_model()
        User.all_objects.create_user(username="alice", password="x", organization=self.orgA)
        User.all_objects.create_user(username="bob", password="x", organization=self.orgB)

    def tearDown(self):
        set_org(None)

    def test_user_objects_scoped_by_org(self):
        set_org(self.orgA.id)
        usernames = list(get_user_model().objects.values_list("username", flat=True))
        self.assertEqual(usernames, ["alice"])

        set_org(self.orgB.id)
        usernames = list(get_user_model().objects.values_list("username", flat=True))
        self.assertEqual(usernames, ["bob"])
