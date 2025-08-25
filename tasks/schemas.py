from ninja import Schema

class TaskOut(Schema):
    id: int
    title: str
    description: str | None
    completed: bool
    priority: int
    metadata: dict
