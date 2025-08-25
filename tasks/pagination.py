# tasks/pagination.py
import base64, json
from datetime import datetime, timezone
from django.db.models import Q

def _b64e(obj: dict) -> str:
    return base64.urlsafe_b64encode(json.dumps(obj, separators=(",", ":")).encode()).decode()

def _b64d(s: str) -> dict:
    return json.loads(base64.urlsafe_b64decode(s.encode()).decode())

def encode_cursor(deadline: datetime | None, priority: int | None, pk: int) -> str:
    d = deadline.astimezone(timezone.utc).isoformat().replace("+00:00", "Z") if deadline else None
    return _b64e({"d": d, "p": priority, "i": pk})

def decode_cursor(cursor: str):
    data = _b64d(cursor)
    d = data.get("d")
    if d:
        # allow fromisoformat with Z
        d = d.replace("Z", "+00:00")
        d = datetime.fromisoformat(d)
    return d, data.get("p"), data["i"]

def rolling_filter(cursor_tuple):
    """
    For ORDER BY deadline DESC, priority DESC, id ASC
    We want rows 'after' the tuple (d,p,i) in that order.
    Equivalent lexicographic filter:
      (deadline < d)
      OR (deadline = d AND priority < p)
      OR (deadline = d AND priority = p AND id > i)
    """
    d, p, i = cursor_tuple
    cond = Q()
    if d is not None:
        cond |= Q(deadline_datetime_with_tz__lt=d)
        if p is not None:
            cond |= Q(deadline_datetime_with_tz=d, priority__lt=p)
            cond |= Q(deadline_datetime_with_tz=d, priority=p, id__gt=i)
        else:
            cond |= Q(deadline_datetime_with_tz=d, id__gt=i)
    else:
        # if previous deadline was NULL, only items with NULL deadline and id>i follow
        cond |= Q(deadline_datetime_with_tz__isnull=True, id__gt=i)
    return cond