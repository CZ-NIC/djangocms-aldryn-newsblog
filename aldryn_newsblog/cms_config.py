from cms.app_base import CMSAppConfig

from .models import Article
from .rendering import render_article_content


class NewsBlogConfig(CMSAppConfig):
    cms_enabled = True
    cms_toolbar_enabled_models = [(Article, render_article_content)]
