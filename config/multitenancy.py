from core.tenant import set_org
from auth.jwt import decode_token
from users.models import User
from django.conf import settings

class OrganizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            org_id = None

            # 1) if session auth is active
            user = getattr(request, "user", None)
            if getattr(user, "is_authenticated", False):
                org_id = user.organization_id
            else:
                # 2) check Authorization: Bearer <token>
                auth_header = request.META.get("HTTP_AUTHORIZATION", "")
                if auth_header.startswith("Bearer "):
                    token = auth_header.split(" ", 1)[1]
                    try:
                        data = decode_token(token)
                        uid = int(data["sub"])
                        org_id = data.get("org")
                        request.user = User.all_objects.get(pk=int(data["sub"]))
                    except Exception as e:
                        # invalid/expired token → leave user unauthenticated
                        print("JWT Decode failed:", e)
                        request.user = None
                        org_id = None

            # 3) fallback (only for dev/testing)
            if settings.DEBUG and not org_id:
                q = request.GET.get("org_id")
                if q and q.isdigit():
                    org_id = int(q)

            set_org(org_id)
            return self.get_response(request)
        finally:
            set_org(None)
