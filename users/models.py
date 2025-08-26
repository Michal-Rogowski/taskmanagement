from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.db import models
from core.tenant import get_org


class TenantUserManager(DjangoUserManager):
    def get_queryset(self):
        qs = super().get_queryset()
        org_id = get_org()
        return qs.filter(organization_id=org_id) if org_id else qs.none()

class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="users",
        null=False,
        blank=False,
    )
    objects = TenantUserManager()
    all_objects = DjangoUserManager()
