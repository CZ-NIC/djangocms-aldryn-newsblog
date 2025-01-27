from django.test import RequestFactory, TestCase

from aldryn_newsblog.cms_appconfig import NewsBlogConfig
from aldryn_newsblog.maintenance import healthcheck


class TestHealthcheck(TestCase):

    def test_fnc(self):
        request = RequestFactory().request
        healthcheck(request)

    def test_fnc_raise(self):
        request = RequestFactory().request
        NewsBlogConfig.objects.get_queryset().delete()
        with self.assertRaisesMessage(RuntimeError, "not NewsBlogConfig.objects.count()"):
            healthcheck(request)
