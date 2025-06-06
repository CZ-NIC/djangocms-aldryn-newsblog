from datetime import timedelta

from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import override

from aldryn_newsblog.feeds import CategoryFeed, LatestArticlesFeed, TagFeed

from . import NewsBlogTransactionTestCase


class TestFeeds(NewsBlogTransactionTestCase):

    def test_latest_feeds(self):
        article = self.create_article()
        future_article = self.create_article(
            publishing_date=now() + timedelta(days=3),
            is_published=True,
        )
        url = reverse(
            f'{self.app_config.namespace}:article-list-feed'
        )
        self.request = self.get_request('en', url)
        self.request.current_page = self.page
        feed = LatestArticlesFeed()(self.request)

        self.assertContains(feed, article.title)
        self.assertNotContains(feed, future_article.title)

    def test_tag_feed(self):
        articles = self.create_tagged_articles()

        url = reverse(
            f'{self.app_config.namespace}:article-list-by-tag-feed',
            args=['tag1']
        )
        self.request = self.get_request('en', url)
        if getattr(self.request, 'current_page', None) is None:
            self.request.current_page = self.page
        feed = TagFeed()(self.request, 'tag1')

        for article in articles['tag1']:
            self.assertContains(feed, article.title)
        for different_tag_article in articles['tag2']:
            self.assertNotContains(feed, different_tag_article.title)

    def test_category_feed(self):
        lang = self.category1.get_current_language()
        with override(lang):
            article = self.create_article()
            article.categories.add(self.category1)
            different_category_article = self.create_article()
            different_category_article.categories.add(self.category2)
            url = reverse(
                '{}:article-list-by-category-feed'.format(
                    self.app_config.namespace),
                args=[self.category1.slug]
            )
            self.request = self.get_request(lang, url)
            if getattr(self.request, 'current_page', None) is None:
                self.request.current_page = self.page

            feed = CategoryFeed()(self.request, self.category1.slug)

            self.assertContains(feed, article.title)
            self.assertNotContains(feed, different_category_article.title)
