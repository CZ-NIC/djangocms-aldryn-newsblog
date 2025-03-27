from django.template.loader import TemplateDoesNotExist, get_template
from django.utils.translation import gettext_lazy as _

from cms import __version__ as cms_version
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from looseversion import LooseVersion

from . import forms, models
from .utils import add_prefix_to_path, default_reverse


CMS_GTE_330 = LooseVersion(cms_version) >= LooseVersion('3.3.0')


class TemplatePrefixMixin:

    def get_render_template(self, context, instance, placeholder) -> str:
        if (hasattr(instance, 'app_config') and instance.app_config.template_prefix):  # noqa: W504
            template_name = add_prefix_to_path(self.render_template, instance.app_config.template_prefix)
            try:
                get_template(template_name)
                return template_name
            except TemplateDoesNotExist:
                pass
        return self.render_template


class NewsBlogPlugin(TemplatePrefixMixin, CMSPluginBase):
    module = 'News & Blog'

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        if hasattr(instance, 'app_config'):
            context['aldryn_newsblog_display_author_no_photo'] = instance.app_config.author_no_photo
            context['aldryn_newsblog_hide_author'] = instance.app_config.hide_author
            context['aldryn_newsblog_template_prefix'] = instance.app_config.template_prefix
        return context


class AdjustableCacheMixin:
    """
    For django CMS < 3.3.0 installations, we have no choice but to disable the
    cache where there is time-sensitive information. However, in later CMS
    versions, we can configure it with `get_cache_expiration()`.
    """
    if not CMS_GTE_330:
        cache = False

    def get_cache_expiration(self, request, instance, placeholder):
        return getattr(instance, 'cache_duration', 0)

    def get_fieldsets(self, request, obj=None):
        """
        Removes the cache_duration field from the displayed form if we're not
        using django CMS v3.3.0 or later.
        """
        fieldsets = super().get_fieldsets(request, obj=None)
        if CMS_GTE_330:
            return fieldsets

        field = 'cache_duration'
        for fieldset in fieldsets:
            new_fieldset = [
                item for item in fieldset[1]['fields'] if item != field]
            fieldset[1]['fields'] = tuple(new_fieldset)
        return fieldsets


@plugin_pool.register_plugin
class NewsBlogArchivePlugin(AdjustableCacheMixin, NewsBlogPlugin):
    render_template = 'aldryn_newsblog/plugins/archive.html'
    name = _('Archive')
    model = models.NewsBlogArchivePlugin
    form = forms.NewsBlogArchivePluginForm

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        request = context.get('request')
        context['instance'] = instance

        queryset = models.Article.objects

        context['dates'] = queryset.get_months(
            request,
            namespace=instance.app_config.namespace
        )
        return context


@plugin_pool.register_plugin
class NewsBlogArticleSearchPlugin(NewsBlogPlugin):
    render_template = 'aldryn_newsblog/plugins/article_search.html'
    name = _('Article Search')
    model = models.NewsBlogArticleSearchPlugin
    form = forms.NewsBlogArticleSearchPluginForm

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        context['instance'] = instance
        context['query_url'] = default_reverse('{}:article-search'.format(
            instance.app_config.namespace), default=None)
        return context


@plugin_pool.register_plugin
class NewsBlogAuthorsPlugin(NewsBlogPlugin):
    render_template = 'aldryn_newsblog/plugins/authors.html'
    name = _('Authors')
    model = models.NewsBlogAuthorsPlugin
    form = forms.NewsBlogAuthorsPluginForm

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        request = context.get('request')
        context['instance'] = instance
        context['authors_list'] = instance.get_authors(request)
        context['article_list_url'] = default_reverse(
            f'{instance.app_config.namespace}:article-list',
            default=None)

        return context


@plugin_pool.register_plugin
class NewsBlogCategoriesPlugin(NewsBlogPlugin):
    render_template = 'aldryn_newsblog/plugins/categories.html'
    name = _('Categories')
    model = models.NewsBlogCategoriesPlugin
    form = forms.NewsBlogCategoriesPluginForm
    cache = False

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        request = context.get('request')
        context['instance'] = instance
        context['categories'] = instance.get_categories(request)
        context['article_list_url'] = default_reverse(
            f'{instance.app_config.namespace}:article-list',
            default=None)
        return context


@plugin_pool.register_plugin
class NewsBlogFeaturedArticlesPlugin(NewsBlogPlugin):
    render_template = 'aldryn_newsblog/plugins/featured_articles.html'
    name = _('Featured Articles')
    model = models.NewsBlogFeaturedArticlesPlugin
    form = forms.NewsBlogFeaturedArticlesPluginForm

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        request = context.get('request')
        context['instance'] = instance
        context['articles_list'] = instance.get_articles(request)
        return context


@plugin_pool.register_plugin
class NewsBlogLatestArticlesPlugin(AdjustableCacheMixin, NewsBlogPlugin):
    render_template = 'aldryn_newsblog/plugins/latest_articles.html'
    name = _('Latest Articles')
    model = models.NewsBlogLatestArticlesPlugin
    form = forms.NewsBlogLatestArticlesPluginForm

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        request = context.get('request')
        context['instance'] = instance
        context['article_list'] = instance.get_articles(request)
        return context


@plugin_pool.register_plugin
class NewsBlogRelatedPlugin(AdjustableCacheMixin, NewsBlogPlugin):
    render_template = 'aldryn_newsblog/plugins/related_articles.html'
    name = _('Related Articles')
    model = models.NewsBlogRelatedPlugin
    form = forms.NewsBlogRelatedPluginForm

    def get_article(self, request):
        if request and request.resolver_match:
            view_name = request.resolver_match.view_name
            namespace = request.resolver_match.namespace
            if view_name == f'{namespace}:article-detail':
                article = models.Article.objects.active_translations(
                    slug=request.resolver_match.kwargs['slug'])
                if article.count() == 1:
                    return article[0]
        return None

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        request = context.get('request')
        context['instance'] = instance
        article = self.get_article(request)
        if article:
            context['article'] = article
            context['article_list'] = instance.get_articles(article, request)
        return context


@plugin_pool.register_plugin
class NewsBlogTagsPlugin(NewsBlogPlugin):
    render_template = 'aldryn_newsblog/plugins/tags.html'
    name = _('Tags')
    model = models.NewsBlogTagsPlugin
    form = forms.NewsBlogTagsPluginForm

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        request = context.get('request')
        context['instance'] = instance
        context['tags'] = instance.get_tags(request)
        context['article_list_url'] = default_reverse(
            f'{instance.app_config.namespace}:article-list',
            default=None)
        return context


@plugin_pool.register_plugin
class NewsBlogSerialEpisodesPlugin(AdjustableCacheMixin, NewsBlogPlugin):
    render_template = 'aldryn_newsblog/plugins/serial_episodes.html'
    name = _('Serial episodes')

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        article = context.get('article')
        if article is not None and article.serial is not None:
            context['serial_episodes'] = article.serial.article_set.exclude(pk=article.pk).order_by('episode')
        return context
