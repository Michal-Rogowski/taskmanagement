from ninja import Router, Schema
from django.contrib.auth import authenticate
from auth.jwt import create_token
from ninja.errors import HttpError 

router = Router(tags=["auth"])

class LoginIn(Schema):
    username: str
    password: str

class TokenOut(Schema):
    access_token: str
    token_type: str = "Bearer"

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