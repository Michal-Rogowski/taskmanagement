from datetime import datetime, timedelta, timezone

import jwt
from django.conf import settings
from django.http import HttpResponse
from django.test import RequestFactory, TestCase

from auth.jwt import ALGO
from config.multitenancy import OrganizationMiddleware
from core.tenant import get_org
from users.models import Organization, User


class OrganizationMiddlewareTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.org1 = Organization.objects.create(name="Org 1")
        self.org2 = Organization.objects.create(name="Org 2")
        self.user = User.objects.create_user(
            username="alice", password="pass", organization=self.org1
        )

    def _mismatched_token(self) -> str:
        now = datetime.now(tz=timezone.utc)
        payload = {
            "sub": str(self.user.id),
            "org": self.org2.id,  # mismatched org claim
            "username": self.user.username,
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(minutes=5)).timestamp()),
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGO)

    def test_mismatched_org_claim_rejected(self):
        token = self._mismatched_token()
        request = self.factory.get("/", HTTP_AUTHORIZATION=f"Bearer {token}")

        captured = {}

        def get_response(req):
            captured["user"] = getattr(req, "user", None)
            captured["org"] = get_org()
            return HttpResponse("ok")

        middleware = OrganizationMiddleware(get_response)
        middleware(request)

        self.assertIsNone(captured["user"])
        self.assertIsNone(captured["org"])
