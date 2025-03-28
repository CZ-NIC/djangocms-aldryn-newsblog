from typing import Any, Dict

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
