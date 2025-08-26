from ninja import Router, Schema
from ninja.errors import HttpError
from django.contrib.auth import get_user_model

router = Router(tags=["users"])
User = get_user_model()

class UserOut(Schema):
    id: int
    username: str

class UserIn(Schema):
    username: str
    password: str

@router.get("/", response=list[UserOut])
def list_users(request):
    u = getattr(request, "user", None)
    if not getattr(u, "is_authenticated", False):
        raise HttpError(401, "Unauthorized")
    qs = User.objects.filter(organization=u.organization).order_by("id")
    return [UserOut(id=i.id, username=i.username) for i in qs]

@router.post("/", response={201: UserOut})
def create_user(request, payload: UserIn):
    u = getattr(request, "user", None)
    if not getattr(u, "is_authenticated", False):
        raise HttpError(401, "Unauthorized")
    if not payload.username or not payload.password:
        raise HttpError(400, "username and password required")
    if User.objects.filter(username=payload.username).exists():
        raise HttpError(400, "username already taken")
    nu = User.objects.create_user(
        username=payload.username,
        password=payload.password,
        organization=u.organization,
    )
    return 201, UserOut(id=nu.id, username=nu.username)
