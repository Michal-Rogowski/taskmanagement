from ninja import Router, Schema
from django.contrib.auth import authenticate, get_user_model
from auth.jwt import create_token
from ninja.errors import HttpError

router = Router(tags=["auth"])
User = get_user_model()

class LoginIn(Schema):
    username: str
    password: str

class TokenOut(Schema):
    access_token: str
    token_type: str = "Bearer"


class RegisterIn(Schema):
    username: str
    password: str

@router.post("/login", response=TokenOut)
def login(request, payload: LoginIn):
    user = authenticate(request, username=payload.username, password=payload.password)
    if not user:
        raise HttpError(401, "Invalid credentials")
    return {"access_token": create_token(user, minutes=60*8)}

@router.get("/me")
def me(request):
    u = getattr(request, "user", None)
    if not getattr(u, "is_authenticated", False):
        raise HttpError(401, "Unauthorized")
    return {"id": u.id, "username": u.username, "organization_id": u.organization_id}


@router.post("/register", response={201: TokenOut})
def register(request, payload: RegisterIn):
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
    return 201, {"access_token": create_token(nu, minutes=60 * 8)}
