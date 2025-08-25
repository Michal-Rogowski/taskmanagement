from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from core.tenant import get_org 

class TenantManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        org_id = get_org()
        return qs.filter(organization_id=org_id) if org_id else qs.none()

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)
    deadline_datetime_with_tz = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = TenantManager()          # ← always tenant-scoped
    all_objects = models.Manager()     # ← unscoped (admin/scripts)
    organization = models.ForeignKey("users.Organization", on_delete=models.CASCADE, related_name="tasks")
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name="tasks")

    metadata = models.JSONField(default=dict, blank=True)

    def clean(self):
        if self.assigned_to and self.assigned_to.organization_id != self.organization_id:
            raise ValidationError("assigned_to must belong to the same organization.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=["organization", "deadline_datetime_with_tz"], name="org_deadline_idx"),
        ]
