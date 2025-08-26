from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Admin for Task model with organization-based query filtering."""

    def get_queryset(self, request):
        # Use the unscoped manager to access all objects and then filter by the
        # organization associated with the requesting user.
        qs = Task.all_objects.all()
        if request.user.is_superuser:
            return qs
        return qs.filter(organization=request.user.organization)
