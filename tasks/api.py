from ninja import Router
from ninja.pagination import paginate, PageNumberPagination
from .models import Task
from .schemas import TaskOut
import json

router = Router()

def _coerce(v: str):
    try:
        return json.loads(v)          # 21 -> 21, true -> True, null -> None
    except Exception:
        return v                       # leave as string if not JSON

@router.get("/", response=list[TaskOut])
@paginate(PageNumberPagination, page_size=10)
def list_tasks(request):
    qs = Task.objects.all()
    user = getattr(request, "user", None)
    if getattr(user, "is_authenticated", False) and getattr(user, "organization_id", None):
        qs = qs.filter(organization=user.organization)

    for key, value in request.GET.items():
        if key.startswith("metadata[") and key.endswith("]"):
            field = key[len("metadata["):-1]
            qs = qs.filter(**{f"metadata__{field}": _coerce(value)})

    return qs
