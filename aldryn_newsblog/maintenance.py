"""
Add into settings:

HEALTHCHECK_FUNCTIONS = [
    "aldryn_newsblog.maintenance.healthcheck",
    ...
]
"""
from django.http import HttpRequest

from .cms_appconfig import NewsBlogConfig
from .models import Article


def healthcheck(request: HttpRequest, *args, **kwargs) -> None:
    """Checking that the system is functional."""
    Article.objects.count()
    if not NewsBlogConfig.objects.count():
        raise RuntimeError('not NewsBlogConfig.objects.count()')
