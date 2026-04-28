from collections.abc import Iterable
from typing import Any, Dict

import django
from django import template
from django.template.loader import TemplateDoesNotExist, get_template


register = template.Library()

_verified_templates = []


@register.simple_tag(takes_context=True)
def prepend_prefix_if_exists(context: Dict[str, Any], path_and_name: str) -> str:
    """Resolve template prefix."""
    prefix = context.get("aldryn_newsblog_template_prefix")
    if prefix is None:
        return f"aldryn_newsblog/{path_and_name}"
    for path in (
        f"aldryn_newsblog/{prefix}/{path_and_name}",
        f"aldryn_newsblog/{path_and_name}",
    ):
        if path in _verified_templates:
            break
        try:
            get_template(path)
            _verified_templates.append(path)
            break
        except TemplateDoesNotExist:
            pass
    return path


if django.VERSION < (5, 0):

    @register.simple_tag(name="querystring", takes_context=True)
    def querystring(context, query_dict=None, **kwargs):
        """
        Add, remove, and change parameters of a ``QueryDict`` and return the result
        as a query string. If the ``query_dict`` argument is not provided, default
        to ``request.GET``.

        For example::

            {% querystring foo=3 %}

        To remove a key::

            {% querystring foo=None %}

        To use with pagination::

            {% querystring page=page_obj.next_page_number %}

        A custom ``QueryDict`` can also be used::

            {% querystring my_query_dict foo=3 %}
        """
        if query_dict is None:
            query_dict = context.request.GET
        params = query_dict.copy()
        for key, value in kwargs.items():
            if value is None:
                if key in params:
                    del params[key]
            elif isinstance(value, Iterable) and not isinstance(value, str):
                params.setlist(key, value)
            else:
                params[key] = value
        if not params and not query_dict:
            return ""
        query_string = params.urlencode()
        return f"?{query_string}"
