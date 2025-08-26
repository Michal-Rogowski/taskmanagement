import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings

ALGO = "HS256"

def create_token(user, minutes: int = 60):
    now = datetime.now(tz=timezone.utc)
    payload = {
        "sub": str(user.id),
        "org": user.organization_id,
        "username": user.username,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=minutes)).timestamp()),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGO)

def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGO])
