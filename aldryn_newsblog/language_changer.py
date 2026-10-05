from django.urls import NoReverseMatch, Resolver404, resolve, reverse
from django.utils import translation
from django.utils.translation import get_language_from_path

from menus.utils import DefaultLanguageChanger

from aldryn_newsblog.models import Category


class LanguageChanger(DefaultLanguageChanger):
    """Aldryn News language changer."""

    def __call__(self, lang):
        try:
            match = resolve(self.request.path)
        except Resolver404:
            return super().__call__(lang)
        kwargs = match.kwargs.copy()
        if slug := kwargs.get("category"):
            language = get_language_from_path(self.request.path_info)
            try:
                category = Category.objects.get(translations__slug=slug, translations__language_code=language)
                kwargs["category"] = category.translations.get(language_code=lang).slug
            except Category.DoesNotExist:
                return super().__call__(lang)
        with translation.override(lang):
            try:
                path = reverse(match.view_name, args=match.args, kwargs=kwargs)
                if self.request.META.get("QUERY_STRING"):
                    path += "?" + self.request.META["QUERY_STRING"]
                return path
            except NoReverseMatch:
                pass
        return super().__call__(lang)
