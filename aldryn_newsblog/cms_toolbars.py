from django.contrib.contenttypes.models import ContentType
from django.urls import Resolver404, resolve, reverse
from django.utils.translation import get_language_from_request
from django.utils.translation import gettext as _
from django.utils.translation import override

from cms.models.contentmodels import PageContent
from cms.toolbar.items import ButtonList
from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool

from aldryn_translation_tools.utils import get_admin_url

from aldryn_newsblog.cms_appconfig import NewsBlogConfig

from .models import Article


@toolbar_pool.register
class NewsBlogToolbar(CMSToolbar):
    # watch_models must be a list, not a tuple
    # see https://github.com/divio/django-cms/issues/4135
    watch_models = [Article]
    supported_apps = ['aldryn_newsblog']

    def get_on_delete_redirect_url(self, article: Article, language: str) -> str:
        """Get on_delete_redirect url."""
        with override(language):
            return reverse(f'{article.app_config.namespace}:article-list')

    def populate(self):
        if not self.is_current_app:
            return

        label = _("NewsBlog")
        config = None
        if self.request.current_page.application_namespace is not None:
            try:
                config = NewsBlogConfig.objects.get(namespace=self.request.current_page.application_namespace)
                label = f"{label} – {config}"
            except NewsBlogConfig.DoesNotExist:
                pass

        menu = self.toolbar.get_or_create_menu('newsblog-app', label)

        user = getattr(self.request, 'user', None)
        change_config_perm = user is not None and user.has_perm('aldryn_newsblog.change_newsblogconfig')
        change_article_perm = user is not None and user.has_perm('aldryn_newsblog.change_article')
        delete_article_perm = user is not None and user.has_perm('aldryn_newsblog.delete_article')
        add_article_perm = user is not None and user.has_perm('aldryn_newsblog.add_article')

        language = get_language_from_request(self.request, check_path=True)

        if config is not None and change_config_perm:
            url = get_admin_url('aldryn_newsblog_newsblogconfig_change', [config.pk], language=language)
            menu.add_modal_item(_('Configure addon'), url=url)
            menu.add_break()

        if change_article_perm:
            params = {} if config is None else {"app_config__id__exact": config.pk}
            url = get_admin_url('aldryn_newsblog_article_changelist', **params)
            menu.add_sideframe_item(_('Article list'), url=url)

        if add_article_perm:
            params = {"language": language} if config is None else {"language": language, "app_config": config.pk}
            if user is not None:
                params["owner"] = user.pk
            menu.add_modal_item(_('Add new article'), url=get_admin_url('aldryn_newsblog_article_add', **params))

        if self.request.resolver_match.url_name == "article-detail" and \
                "aldryn_newsblog" in self.request.resolver_match.app_names:
            obj = self.request.toolbar.get_object()
            if obj and isinstance(obj, Article):
                if change_article_perm:
                    change_article_url = get_admin_url('aldryn_newsblog_article_change', [obj.pk], language=language)
                    menu.add_modal_item(_('Edit this article'), url=change_article_url, active=True)

                if delete_article_perm:
                    redirect_url = self.get_on_delete_redirect_url(obj, language=language)
                    url = get_admin_url('aldryn_newsblog_article_delete', [obj.pk])
                    menu.add_modal_item(_('Delete this article'), url=url, on_close=redirect_url)
        try:
            self.enable_edit_page_content(language)
        except (ContentType.DoesNotExist, PageContent.DoesNotExist):
            pass

    def enable_edit_page_content(self, language: str) -> None:
        """Enable edit PageContent."""
        try:
            view_func, args, kwargs = resolve(self.request.path)
        except Resolver404:
            content_type_obj = PageContent.objects.get(page=self.request.current_page, language=language)
        else:
            if view_func.__name__ in ("render_object_edit", "render_object_preview") and len(args) == 2:
                content_type_id, object_id = args
                content_type = ContentType.objects.get_for_id(content_type_id)
                model = content_type.model_class()
                if not issubclass(model, PageContent):
                    return
                if "render_object_edit":
                    content_type_obj = model.admin_manager.select_related("page").get(pk=object_id)
                else:
                    content_type_obj = model.objects.select_related("page").get(pk=object_id)
            else:
                content_type_obj = PageContent.objects.get(page=self.request.current_page, language=language)
        self.toolbar.set_object(content_type_obj)

    def post_template_populate(self):
        # Disable call self.add_wizard_button().
        self.render_object_editable_buttons()

    def render_object_editable_buttons(self):
        self.add_article_button()

    def add_article_button(self):
        obj = self.request.toolbar.get_object()
        if obj is None or not isinstance(obj, Article):
            return
        with override(get_language_from_request(self.request)):
            url = obj.get_absolute_url()
        item = ButtonList(side=self.toolbar.RIGHT)
        item.add_button(
            _('View Published'),
            url=url,
            disabled=False,
            extra_classes=['cms-btn'],
        )
        self.toolbar.add_item(item)
