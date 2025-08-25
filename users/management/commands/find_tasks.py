from django.core.management.base import BaseCommand, CommandError
from tasks.models import Task

class Command(BaseCommand):
    help = "Find tasks by org and dynamic metadata filters (key=value). Supports lookups like key__gt=5"

    def add_arguments(self, parser):
        parser.add_argument("--org", required=True, help="Organization name")
        parser.add_argument("--meta", action="append", default=[],
                            help="Repeatable metadata filter: key=value (supports lookups, e.g. story_points__gt=5)")
        parser.add_argument("--order-by", default="id",
                            help="Ordering field (e.g. -created_at, metadata__priority)")
        parser.add_argument("--limit", type=int, default=20, help="Max results")

    def handle(self, *args, **opts):
        org = opts["org"]
        metas = opts["meta"]
        order_by = opts["order_by"]
        limit = opts["limit"]

        qs = Task.all_objects.filter(organization__name=org)

        for item in metas:
            if "=" not in item:
                raise CommandError(f"Invalid --meta '{item}'. Use key=value.")
            key, value = item.split("=", 1)
            if value.isdigit():
                value_cast = int(value)
            elif value.lower() in ("true", "false"):
                value_cast = value.lower() == "true"
            else:
                value_cast = value
            qs = qs.filter(**{f"metadata__{key}": value_cast})

        qs = qs.order_by(order_by)[:limit]

        if not qs.exists():
            self.stdout.write("No results.")
            return

        for t in qs:
            self.stdout.write(f"[{t.id}] {t.title} | completed={t.completed} | meta={t.metadata}")
