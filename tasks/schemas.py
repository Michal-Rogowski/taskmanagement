from ninja import Schema
from typing import Any

class TaskOut(Schema):
    id: int
    title: str
    description: str | None
    completed: bool
    priority: int
    metadata: dict[str, Any]
    deadline_datetime_with_tz: str | None

class TaskIn(Schema):
    title: str
    description: str | None = None
    completed: bool = False
    priority: int = 0
    deadline_datetime_with_tz: str | None = None
    assigned_to_id: int | None = None
    metadata: dict[str, Any] = {}

class TaskUpdate(Schema):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None
    priority: int | None = None
    deadline_datetime_with_tz: str | None = None
    assigned_to_id: int | None = None
    metadata: dict[str, Any] | None = None

class CursorPage(Schema):
    items: list[TaskOut]
    next_cursor: str | None
    limit: int