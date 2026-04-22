from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from . import models


DEFAULT_CHOICES = (("", ""),)


class AutoAppConfigFormMixin:
    """
    If there is only a single AppConfig to choose, automatically select it.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'app_config' in self.fields:
            # if has only one choice, select it by default
            if self.fields['app_config'].queryset.count() == 1:
                self.fields['app_config'].empty_label = None


class NewsBlogArchivePluginForm(AutoAppConfigFormMixin, forms.ModelForm):

    template_list = forms.ChoiceField(
        label=_("Template list"),
        required=False,
        choices=getattr(settings, "ALDRYN_NEWSBLOG_TEMPLATES_ARCHIVE", DEFAULT_CHOICES),
        help_text="settings.ALDRYN_NEWSBLOG_TEMPLATES_ARCHIVE"
    )

    class Meta:
        model = models.NewsBlogArchivePlugin
        fields = ['app_config', 'cache_duration', 'template_list']


class NewsBlogArticleSearchPluginForm(AutoAppConfigFormMixin, forms.ModelForm):

    template_list = forms.ChoiceField(
        label=_("Template list"),
        required=False,
        choices=getattr(settings, "ALDRYN_NEWSBLOG_TEMPLATES_SEARCH", DEFAULT_CHOICES),
        help_text="settings.ALDRYN_NEWSBLOG_TEMPLATES_SEARCH"
    )

    class Meta:
        model = models.NewsBlogArticleSearchPlugin
        fields = ['app_config', 'max_articles', 'template_list']


class NewsBlogAuthorsPluginForm(AutoAppConfigFormMixin, forms.ModelForm):

    template_list = forms.ChoiceField(
        label=_("Template list"),
        required=False,
        choices=getattr(settings, "ALDRYN_NEWSBLOG_TEMPLATES_AUTHORS", DEFAULT_CHOICES),
        help_text="settings.ALDRYN_NEWSBLOG_TEMPLATES_AUTHORS"
    )

    class Meta:
        model = models.NewsBlogAuthorsPlugin
        fields = ['app_config', 'template_list']


class NewsBlogCategoriesPluginForm(AutoAppConfigFormMixin, forms.ModelForm):

    template_list = forms.ChoiceField(
        label=_("Template list"),
        required=False,
        choices=getattr(settings, "ALDRYN_NEWSBLOG_TEMPLATES_CATEGORIES", DEFAULT_CHOICES),
        help_text="settings.ALDRYN_NEWSBLOG_TEMPLATES_CATEGORIES"
    )

    class Meta:
        model = models.NewsBlogCategoriesPlugin
        fields = ['app_config', 'template_list']


class NewsBlogFeaturedArticlesPluginForm(AutoAppConfigFormMixin,
                                         forms.ModelForm):

    template_list = forms.ChoiceField(
        label=_("Template list"),
        required=False,
        choices=getattr(settings, "ALDRYN_NEWSBLOG_TEMPLATES_FEATURED_ARTICLES", DEFAULT_CHOICES),
        help_text="settings.ALDRYN_NEWSBLOG_TEMPLATES_FEATURED_ARTICLES"
    )

    class Meta:
        model = models.NewsBlogFeaturedArticlesPlugin
        fields = ['app_config', 'article_count', 'template_list']


class NewsBlogLatestArticlesPluginForm(AutoAppConfigFormMixin,
                                       forms.ModelForm):

    template_list = forms.ChoiceField(
        label=_("Template list"),
        required=False,
        choices=getattr(settings, "ALDRYN_NEWSBLOG_TEMPLATES_LATEST_ARTICLES", DEFAULT_CHOICES),
        help_text="settings.ALDRYN_NEWSBLOG_TEMPLATES_LATEST_ARTICLES"
    )

    class Meta:
        model = models.NewsBlogLatestArticlesPlugin
        fields = [
            'app_config', 'latest_articles', 'exclude_featured',
            'cache_duration', 'template_list'
        ]


class NewsBlogTagsPluginForm(AutoAppConfigFormMixin, forms.ModelForm):

    template_list = forms.ChoiceField(
        label=_("Template list"),
        required=False,
        choices=getattr(settings, "ALDRYN_NEWSBLOG_TEMPLATES_TAGS", DEFAULT_CHOICES),
        help_text="settings.ALDRYN_NEWSBLOG_TEMPLATES_TAGS"
    )

    class Meta:
        fields = ['app_config', 'template_list']


class NewsBlogRelatedPluginForm(forms.ModelForm):
    class Meta:
        fields = ['cache_duration']
