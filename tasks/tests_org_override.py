import os
from django.test import TestCase, RequestFactory, override_settings
from django.http import HttpResponse
from users.models import Organization
from core.tenant import get_org
from config.multitenancy import OrganizationMiddleware


class OrgOverrideFlagTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.org = Organization.objects.create(name="OrgA")

    def _call_mw(self, query: str):
        captured = {}

        def get_response(request):
            captured["org"] = get_org()
            return HttpResponse("ok")

        mw = OrganizationMiddleware(get_response)
        request = self.factory.get(f"/?{query}")
        request.user = None
        with override_settings(DEBUG=True):
            mw(request)
        return captured.get("org")

    def test_query_param_used_only_with_flag(self):
        # Without flag the override should be ignored
        os.environ.pop("ALLOW_ORG_OVERRIDE", None)
        org_id = self._call_mw(f"org_id={self.org.id}")
        self.assertIsNone(org_id)

        # With flag the override is honored
        os.environ["ALLOW_ORG_OVERRIDE"] = "1"
        org_id = self._call_mw(f"org_id={self.org.id}")
        self.assertEqual(org_id, self.org.id)
        os.environ.pop("ALLOW_ORG_OVERRIDE", None)
