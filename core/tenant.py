from contextvars import ContextVar
_current_org = ContextVar("current_org", default=None)

def set_org(org_id: int | None): _current_org.set(org_id)
def get_org() -> int | None:     return _current_org.get()