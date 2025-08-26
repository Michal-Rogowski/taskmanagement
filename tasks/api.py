import json
from django.utils.dateparse import parse_datetime
from ninja import Router
from ninja.errors import HttpError
from .models import Task
from .schemas import TaskOut, TaskIn, TaskUpdate, CursorPage
from tasks.pagination import encode_cursor, decode_cursor, rolling_filter
from ninja.responses import Response

router = Router()


def _require_auth(request):
    """Ensure the request user is authenticated or raise 401."""
    user = getattr(request, "user", None)
    if not getattr(user, "is_authenticated", False):
        raise HttpError(401, "Unauthorized")
    return user

def _coerce(v: str):
    try:
        return json.loads(v)
    except Exception:
        return v

def _apply_metadata_filters(qs, request):
    for key, value in request.GET.items():
        if key.startswith("metadata[") and key.endswith("]"):
            field = key[len("metadata["):-1]
            if "__" not in field:
                field = (field.replace("_gte", "__gte")
                              .replace("_lte", "__lte")
                              .replace("_gt", "__gt")
                              .replace("_lt", "__lt"))
            qs = qs.filter(**{f"metadata__{field}": _coerce(value)})
    return qs

def _parse_dt(dt_str: str | None):
    if not dt_str:
        return None
    dt = parse_datetime(dt_str)
    if not dt:
        raise HttpError(400, "Invalid datetime format. Use ISO 8601.")
    return dt

@router.get("/", response=CursorPage)
def list_tasks(request, limit: int = 20, cursor: str | None = None):
    _require_auth(request)
    # Tenant scoping is done by Task.objects (TenantManager)
    qs = Task.objects.all()
    qs = _apply_metadata_filters(qs, request)

    # Order: deadline DESC, priority DESC, id ASC
    qs = qs.order_by(
        "-deadline_datetime_with_tz",
        "-priority",
        "id",
    )

    if cursor:
        d, p, i = decode_cursor(cursor)
        qs = qs.filter(rolling_filter((d, p, i)))

    items = list(qs[:limit])
    if not items:
        return {"items": [], "next_cursor": None, "limit": limit}

    last = items[-1]
    next_cursor = encode_cursor(
        last.deadline_datetime_with_tz, last.priority, last.id
    )

    # serialize
    out = []
    for t in items:
        out.append(TaskOut(
            id=t.id, title=t.title, description=t.description,
            completed=t.completed, priority=t.priority,
            metadata=t.metadata,
            deadline_datetime_with_tz=(
                t.deadline_datetime_with_tz.isoformat() if t.deadline_datetime_with_tz else None
            ),
        ))

    return {"items": out, "next_cursor": next_cursor, "limit": limit}

@router.post("/", response={201: TaskOut})
def create_task(request, payload: TaskIn):
    user = _require_auth(request)
    org = user.organization

    assigned = None
    if payload.assigned_to_id:
        from users.models import User
        try:
            assigned = User.objects.get(pk=payload.assigned_to_id)
        except User.DoesNotExist:
            raise HttpError(400, "assigned_to_id not found")
        if assigned.organization_id != org.id:
            raise HttpError(400, "assigned_to must belong to your organization")

    t = Task.all_objects.create(
        title=payload.title,
        description=payload.description or "",
        completed=payload.completed,
        priority=payload.priority or 0,
        deadline_datetime_with_tz=_parse_dt(payload.deadline_datetime_with_tz),
        organization=org,
        assigned_to=assigned,
        metadata=payload.metadata or {},
    )
    return 201, TaskOut(
        id=t.id, title=t.title, description=t.description,
        completed=t.completed, priority=t.priority,
        metadata=t.metadata,
        deadline_datetime_with_tz=(
            t.deadline_datetime_with_tz.isoformat() if t.deadline_datetime_with_tz else None
        ),
    )

@router.put("/{task_id}/", response=TaskOut)
def update_task(request, task_id: int, payload: TaskUpdate):
    _require_auth(request)

    # Scoped manager ensures same‑org; 404 if not found
    try:
        t = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise HttpError(404, "Not found")

    if payload.title is not None:
        t.title = payload.title
    if payload.description is not None:
        t.description = payload.description
    if payload.completed is not None:
        t.completed = payload.completed
    if payload.priority is not None:
        t.priority = payload.priority
    if payload.deadline_datetime_with_tz is not None:
        t.deadline_datetime_with_tz = _parse_dt(payload.deadline_datetime_with_tz)
    if payload.metadata is not None:
        t.metadata = payload.metadata
    if payload.assigned_to_id is not None:
        from users.models import User
        if payload.assigned_to_id == 0:
            t.assigned_to = None
        else:
            try:
                assignee = User.objects.get(pk=payload.assigned_to_id)
            except User.DoesNotExist:
                raise HttpError(400, "assigned_to_id not found")
            # validate org
            if assignee.organization_id != t.organization_id:
                raise HttpError(400, "assigned_to must belong to your organization")
            t.assigned_to = assignee

    t.save()
    return TaskOut(
        id=t.id, title=t.title, description=t.description,
        completed=t.completed, priority=t.priority,
        metadata=t.metadata,
        deadline_datetime_with_tz=(
            t.deadline_datetime_with_tz.isoformat() if t.deadline_datetime_with_tz else None
        ),
    )

@router.delete("/{task_id}/")
def delete_task(request, task_id: int):
    _require_auth(request)
    try:
        t = Task.objects.get(pk=task_id)  # scoped → same‑org only
    except Task.DoesNotExist:
        raise HttpError(404, "Not found")
    t.delete()
    return Response(status=204)
