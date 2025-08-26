from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0002_initial"),
    ]

    operations = [
        migrations.RunSQL(
            sql="DROP INDEX IF EXISTS org_deadline_idx",
            reverse_sql="CREATE INDEX org_deadline_idx ON tasks_task (organization_id, deadline_datetime_with_tz)",
        ),
        migrations.AddIndex(
            model_name="task",
            index=models.Index(
                fields=["organization", "deadline_datetime_with_tz", "priority"],
                name="org_deadline_priority_idx",
            ),
        ),
    ]

