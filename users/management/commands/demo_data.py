from django.core.management.base import BaseCommand
from users.models import Organization, User
from tasks.models import Task

class Command(BaseCommand):
    help = "Seed demo data"

    def handle(self, *args, **kwargs):
        org_a, _ = Organization.objects.get_or_create(name="OrgA")
        org_b, _ = Organization.objects.get_or_create(name="OrgB")

        alice, _ = User.all_objects.get_or_create(username="alice", defaults={"organization": org_a})
        if not alice.organization_id:
            alice.organization = org_a
        alice.set_password("1234"); alice.save()

        bob, _ = User.all_objects.get_or_create(username="bob", defaults={"organization": org_b})
        if not bob.organization_id:
            bob.organization = org_b
        bob.set_password("1234"); bob.save()

        Task.objects.get_or_create(title="Fix bug", organization=org_a,
            defaults={"assigned_to": alice, "metadata": {"sprint": 21, "priority": 5}})
        Task.objects.get_or_create(title="Build feat", organization=org_a,
            defaults={"assigned_to": alice, "metadata": {"sprint": 21, "priority": 2}})
        Task.objects.get_or_create(title="Write docs", organization=org_a,
            defaults={"assigned_to": alice, "metadata": {"sprint": 22, "priority": 1}})

        Task.objects.get_or_create(title="Infra setup", organization=org_b,
            defaults={"assigned_to": bob, "metadata": {"sprint": 7, "env": "prod"}})
        Task.objects.get_or_create(title="Cost report", organization=org_b,
            defaults={"assigned_to": bob, "metadata": {"sprint": 7, "budget": 9000}})

        self.stdout.write(self.style.SUCCESS("Demo data created."))
