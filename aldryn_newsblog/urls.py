from django.urls import path, re_path

from aldryn_newsblog.feeds import CategoryFeed, LatestArticlesFeed, TagFeed
from aldryn_newsblog.views import (
    ArticleDetail, ArticleList, ArticleSearchResultsList, AuthorArticleList,
    CategoryArticleList, DayArticleList, MonthArticleList, TagArticleList,
    YearArticleList, YearCategoryArticleList,
)


urlpatterns = [
    path('', ArticleList.as_view(), name='article-list'),

    path('feed/', LatestArticlesFeed(), name='article-list-feed'),

    path('search/', ArticleSearchResultsList.as_view(), name='article-search'),

    re_path(r'^author/(?P<author>\w[-\w]*)/$', AuthorArticleList.as_view(), name='article-list-by-author'),

    re_path(r'^category/(?P<category>\w[-\w]*)/feed/$', CategoryFeed(), name='article-list-by-category-feed'),
    re_path(r'^category/(?P<category>\w[-\w]*)/$', CategoryArticleList.as_view(), name='article-list-by-category'),

    re_path(r'^tag/(?P<tag>\w[-\w]*)/feed/$', TagFeed(), name='article-list-by-tag-feed'),
    re_path(r'^tag/(?P<tag>\w[-\w]*)/$', TagArticleList.as_view(), name='article-list-by-tag'),

    re_path(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', DayArticleList.as_view(),
            name='article-list-by-day'),
    re_path(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$', MonthArticleList.as_view(), name='article-list-by-month'),
    re_path(r'^(?P<year>\d{4})/$', YearArticleList.as_view(), name='article-list-by-year'),
    re_path(r'^year/(?P<year>\d{4})/category/(?P<category>\w[-\w]*)/$', YearCategoryArticleList.as_view(),
            name='article-list-by-year-and-category'),

    # Various permalink styles that we support
    # ----------------------------------------
    # This supports permalinks with <article_pk>
    # NOTE: We cannot support /year/month/pk, /year/pk, or /pk, since these
    # patterns collide with the list/archive views, which we'd prefer to
    # continue to support.
    re_path(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<pk>\d+)/$', ArticleDetail.as_view(),
            name='article-detail'),
    re_path(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>\w[-\w]*)/$',  # flake8: noqa
            ArticleDetail.as_view(), name='article-detail'),
    re_path(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<slug>\w[-\w]*)/$', ArticleDetail.as_view(),
            name='article-detail'),
    re_path(r'^(?P<year>\d{4})/(?P<slug>\w[-\w]*)/$', ArticleDetail.as_view(), name='article-detail'),

    # These support permalinks with <article_slug>
    re_path(r'^(?P<slug>\w[-\w]*)/$', ArticleDetail.as_view(), name='article-detail'),
]
