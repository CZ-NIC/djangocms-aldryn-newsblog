from typing import Optional

from django.contrib import admin
from django.urls.exceptions import NoReverseMatch
from django.utils.translation import gettext_lazy as _

from cms.admin.placeholderadmin import (
    FrontendEditableAdminMixin, PlaceholderAdminMixin,
)

from aldryn_apphooks_config.admin import BaseAppHookConfig, ModelAppHookConfig
from aldryn_people.models import Person
from aldryn_translation_tools.admin import AllTranslationsMixin
from parler.admin import TranslatableAdmin
from parler.forms import TranslatableModelForm

from . import models


def make_published(modeladmin, request, queryset):
    queryset.update(is_published=True)


make_published.short_description = _(
    "Mark selected articles as published")


def make_unpublished(modeladmin, request, queryset):
    queryset.update(is_published=False)


make_unpublished.short_description = _(
    "Mark selected articles as not published")


def make_featured(modeladmin, request, queryset):
    queryset.update(is_featured=True)


make_featured.short_description = _(
    "Mark selected articles as featured")


def make_not_featured(modeladmin, request, queryset):
    queryset.update(is_featured=False)


make_not_featured.short_description = _(
    "Mark selected articles as not featured")


class ArticleAdminForm(TranslatableModelForm):

    class Meta:
        model = models.Article
        fields = [
            'app_config',
            'categories',
            'featured_image',
            'is_featured',
            'is_published',
            'lead_in',
            'meta_description',
            'meta_keywords',
            'meta_title',
            'owner',
            'related',
            'slug',
            'tags',
            'title',
            'serial',
            'episode',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        qs = models.Article.objects
        if self.instance.app_config_id:
            qs = models.Article.objects.filter(
                app_config=self.instance.app_config)
        elif 'initial' in kwargs and 'app_config' in kwargs['initial']:
            qs = models.Article.objects.filter(
                app_config=kwargs['initial']['app_config'])

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if 'related' in self.fields:
            self.fields['related'].queryset = qs

        # Don't allow app_configs to be added here. The correct way to add an
        # apphook-config is to create an apphook on a cms Page.
        self.fields['app_config'].widget.can_add_related = False
        # Don't allow related articles to be added here.
        # doesn't makes much sense to add articles from another article other
        # than save and add another.
        if ('related' in self.fields and  # noqa: W504
                hasattr(self.fields['related'], 'widget')):
            self.fields['related'].widget.can_add_related = False


class ArticleAdmin(
    AllTranslationsMixin,
    PlaceholderAdminMixin,
    FrontendEditableAdminMixin,
    ModelAppHookConfig,
    TranslatableAdmin
):
    form = ArticleAdminForm
    list_display = ('title', 'app_config', 'slug', 'is_featured',
                    'is_published')
    list_filter = [
        'app_config',
        'categories',
    ]
    actions = (
        make_featured, make_not_featured,
        make_published, make_unpublished,
    )
    fieldsets = (
        (None, {
            'fields': (
                'title',
                'author',
                'publishing_date',
                'is_published',
                'is_featured',
                'featured_image',
                'lead_in',
            )
        }),
        (_('Serial Options'), {
            'classes': ('collapse',),
            'fields': (
                'serial',
                'episode',
            )
        }),
        (_('Meta Options'), {
            'classes': ('collapse',),
            'fields': (
                'slug',
                'meta_title',
                'meta_description',
                'meta_keywords',
            )
        }),
        (_('Advanced Settings'), {
            'classes': ('collapse',),
            'fields': (
                'tags',
                'categories',
                'related',
                'owner',
                'app_config',
            )
        }),
    )
    filter_horizontal = [
        'categories',
    ]
    app_config_values = {
        'default_published': 'is_published'
    }
    app_config_selection_title = ''
    app_config_selection_desc = ''

    def add_view(self, request, *args, **kwargs):
        data = request.GET.copy()
        try:
            person = Person.objects.get(user=request.user)
            data['author'] = person.pk
            request.GET = data
        except Person.DoesNotExist:
            pass

        data['owner'] = request.user.pk
        request.GET = data
        return super().add_view(request, *args, **kwargs)

    def get_view_on_site_url(self, obj=None) -> Optional[str]:
        if obj is not None:
            try:
                obj.get_absolute_url()
            except NoReverseMatch:
                # This occurs when Aldryn News section is not published on the site.
                # 'aldryn_newsblog_default' is not a registered namespace
                return None
        return super().get_view_on_site_url(obj)


class SerialAdmin(admin.ModelAdmin):
    list_display = ('name', 'episodes_count')
    change_form_template = "aldryn_newsblog/admin/serial_episodes_change_form.html"

    def episodes_count(self, obj: models.Serial) -> int:
        return models.Article.objects.filter(serial=obj).count()
    episodes_count.short_description = _('Total episodes')

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['serial_episodes'] = models.Article.objects.filter(serial_id=object_id).order_by('episode')
        return self.changeform_view(request, object_id, form_url, extra_context)


admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.Serial, SerialAdmin)


class NewsBlogConfigAdmin(
    AllTranslationsMixin,
    PlaceholderAdminMixin,
    BaseAppHookConfig,
    TranslatableAdmin
):
    def get_config_fields(self):
        return (
            'app_title', 'permalink_type', 'non_permalink_handling',
            'template_prefix', 'paginate_by', 'pagination_pages_start',
            'pagination_pages_visible', 'exclude_featured',
            'create_authors', 'hide_author', 'author_no_photo', 'search_indexed', 'config.default_published',
        )


admin.site.register(models.NewsBlogConfig, NewsBlogConfigAdmin)
