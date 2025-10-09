from django.urls import reverse
from django.utils.translation import get_language_from_request
from django.utils.translation import gettext as _
from django.utils.translation import override

from cms.toolbar.items import ButtonList
from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool

from aldryn_translation_tools.utils import get_admin_url

from .models import Article


@toolbar_pool.register
class NewsBlogToolbar(CMSToolbar):
    # watch_models must be a list, not a tuple
    # see https://github.com/divio/django-cms/issues/4135
    watch_models = [Article, ]
    supported_apps = ('aldryn_newsblog',)

    def get_on_delete_redirect_url(self, article, language):
        with override(language):
            url = reverse(
                f'{article.app_config.namespace}:article-list')
        return url

    def populate(self):
        obj = self.request.toolbar.get_object()
        if not isinstance(obj, Article):
            return
        article = obj
        config = article.app_config

        user = getattr(self.request, 'user', None)
        language = get_language_from_request(self.request, check_path=True)

        menu = self.toolbar.get_or_create_menu('newsblog-app', config.get_app_title())

        change_config_perm = user.has_perm('aldryn_newsblog.change_newsblogconfig')
        add_config_perm = user.has_perm('aldryn_newsblog.add_newsblogconfig')
        config_perms = [change_config_perm, add_config_perm]

        change_article_perm = user.has_perm('aldryn_newsblog.change_article')
        delete_article_perm = user.has_perm('aldryn_newsblog.delete_article')
        add_article_perm = user.has_perm('aldryn_newsblog.add_article')
        article_perms = [change_article_perm, add_article_perm, delete_article_perm, ]

        if change_config_perm:
            url_args = {}
            if language:
                url_args = {'language': language, }
            url = get_admin_url('aldryn_newsblog_newsblogconfig_change', [config.pk, ], **url_args)
            menu.add_modal_item(_('Configure addon'), url=url)

        if any(config_perms) and any(article_perms):
            menu.add_break()

        if change_article_perm:
            url_args = {}
            if config:
                url_args = {'app_config__id__exact': config.pk}
            url = get_admin_url('aldryn_newsblog_article_changelist', **url_args)
            menu.add_sideframe_item(_('Article list'), url=url)

        if add_article_perm:
            url_args = {'app_config': config.pk, 'owner': user.pk, }
            if language:
                url_args.update({'language': language, })
            url = get_admin_url('aldryn_newsblog_article_add', **url_args)
            menu.add_modal_item(_('Add new article'), url=url)

        if change_article_perm and article:
            url_args = {}
            if language:
                url_args = {'language': language, }
            change_article_url = get_admin_url('aldryn_newsblog_article_change', [article.pk, ], **url_args)
            menu.add_modal_item(_('Edit this article'), url=change_article_url, active=True)

        if delete_article_perm and article:
            redirect_url = self.get_on_delete_redirect_url(
                article, language=language)
            url = get_admin_url('aldryn_newsblog_article_delete', [article.pk, ])
            menu.add_modal_item(_('Delete this article'), url=url, on_close=redirect_url)

    def post_template_populate(self):
        # Disable call self.add_wizard_button().
        self.render_object_editable_buttons()

    def render_object_editable_buttons(self):
        self.add_article_button()

    def add_article_button(self):
        article = self.request.toolbar.get_object()
        if article is None:
            return
        with override(get_language_from_request(self.request)):
            url = article.get_absolute_url()
        item = ButtonList(side=self.toolbar.RIGHT)
        item.add_button(
            _('View Published'),
            url=url,
            disabled=False,
            extra_classes=['cms-btn'],
        )
        self.toolbar.add_item(item)
