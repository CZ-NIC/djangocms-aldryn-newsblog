import os

from django.conf import settings
from django.utils.timezone import now
from django.utils.translation import activate, override

from cms import api

from aldryn_newsblog.models import Article

from .mixins import (
    TESTS_STATIC_ROOT, NewsBlogTestCase, NewsBlogTransactionTestCase,
)


FEATURED_IMAGE_PATH = os.path.join(TESTS_STATIC_ROOT, 'featured_image.jpg')


class TestModels(NewsBlogTestCase):

    def test_create_article(self):
        article = self.create_article()
        response = self.client.get(article.get_absolute_url())
        self.assertContains(response, article.title)

    def test_delete_article(self):
        article = self.create_article()
        article_pk = article.pk
        article_url = article.get_absolute_url()
        response = self.client.get(article_url)
        self.assertContains(response, article.title)
        Article.objects.get(pk=article_pk).delete()
        response = self.client.get(article_url)
        self.assertEqual(response.status_code, 404)

    def test_auto_slugifies(self):
        activate(self.language)
        title = 'This is a title'
        author = self.create_person()
        article = Article.objects.create(
            title=title, author=author, owner=author.user,
            app_config=self.app_config, publishing_date=now(),
            is_published=True,
        )
        article.save()
        self.assertEqual(article.slug, 'this-is-a-title')
        # Now, let's try another with the same title
        article_1 = Article(
            title=title.lower(),
            author=author,
            owner=author.user,
            app_config=self.app_config,
            publishing_date=now(),
            is_published=True,
        )
        # Note, it cannot be the exact same title, else we'll fail the unique
        # constraint on the field.
        article_1.save()
        # Note that this should be "incremented" slug here.
        self.assertEqual(article_1.slug, 'this-is-a-title-1')
        article_2 = Article(
            title=title.upper(),
            author=author,
            owner=author.user,
            app_config=self.app_config,
            publishing_date=now(),
            is_published=True,
        )
        article_2.save()
        self.assertEqual(article_2.slug, 'this-is-a-title-2')

    def test_auto_existing_author(self):
        author = self.create_person()
        article = Article.objects.create(
            title=self.rand_str(), owner=author.user,
            app_config=self.app_config, publishing_date=now(),
            is_published=True,
        )
        article.save()
        self.assertEqual(article.author.user, article.owner)

        old = self.app_config.create_authors
        self.app_config.create_authors = False
        self.app_config.save()
        article = Article.objects.create(
            title=self.rand_str(), owner=author.user,
            app_config=self.app_config, publishing_date=now(),
            is_published=True,
        )
        self.app_config.create_authors = old
        self.app_config.save()
        self.assertEqual(article.author, None)

    def test_auto_new_author(self):
        user = self.create_user()
        article = Article.objects.create(
            title=self.rand_str(), owner=user,
            app_config=self.app_config, publishing_date=now(),
            is_published=True,
        )
        article.save()
        self.assertEqual(article.author.name, ' '.join((user.first_name, user.last_name)))

    def test_auto_search_data(self):
        activate(self.language)

        user = self.create_user()

        lead_in = 'Hello! this text will be searchable.'

        Article.update_search_on_save = True

        article = Article.objects.create(
            title=self.rand_str(),
            owner=user,
            lead_in=lead_in,
            app_config=self.app_config,
            publishing_date=now(),
            is_published=True,
        )
        article.save()

        search_data = article.get_search_data()

        self.assertEqual(lead_in, search_data)
        self.assertEqual(article.search_data, search_data)

    def test_auto_search_data_off(self):
        activate(self.language)
        user = self.create_user()

        lead_in = 'Hello! this text will not be searchable.'

        Article.update_search_on_save = False

        article = Article.objects.create(
            title=self.rand_str(),
            owner=user,
            lead_in=lead_in,
            app_config=self.app_config,
            publishing_date=now(),
            is_published=True,
        )
        article.save()

        search_data = article.get_search_data()

        # set it back to true
        Article.update_search_on_save = True

        self.assertEqual(lead_in, search_data)
        self.assertNotEqual(article.search_data, search_data)

    def test_has_content(self):
        # Just make sure we have a known language
        activate(self.language)
        title = self.rand_str()
        content = self.rand_str()
        author = self.create_person()
        article = Article.objects.create(
            title=title, slug=self.rand_str(), author=author, owner=author.user,
            app_config=self.app_config, publishing_date=now(),
            is_published=True,
        )
        article.save()
        api.add_plugin(article.content_placeholder, 'TextPlugin', self.language)
        plugin = article.content_placeholder.get_plugins()[0].get_plugin_instance()[0]
        plugin.body = content
        plugin.save()
        response = self.client.get(article.get_absolute_url())
        self.assertContains(response, title)
        self.assertContains(response, content)

    def test_change_title(self):
        """
        Test that we can change the title of an existing, published article
        without issue. Also ensure that the slug does NOT change when changing
        the title alone.
        """
        activate(self.language)
        initial_title = "This is the initial title"
        initial_slug = "this-is-the-initial-title"
        author = self.create_person()
        article = Article.objects.create(
            title=initial_title, author=author, owner=author.user,
            app_config=self.app_config, publishing_date=now(),
            is_published=True,
        )
        article.save()
        self.assertEqual(article.title, initial_title)
        self.assertEqual(article.slug, initial_slug)
        # Now, let's try to change the title
        new_title = "This is the new title"
        article.title = new_title
        article.save()
        article = self.reload(article)
        self.assertEqual(article.title, new_title)
        self.assertEqual(article.slug, initial_slug)


class TestModelsTransactions(NewsBlogTransactionTestCase):

    def test_duplicate_title_and_language(self):
        """
        Test that if user attempts to create an article with the same name and
        in the same language as another, it will not raise exceptions.
        """
        title = "Sample Article"
        author = self.create_person()
        original_lang = settings.LANGUAGES[0][0]
        # Create an initial article in the first language
        article1 = Article(
            title=title, author=author, owner=author.user,
            app_config=self.app_config, publishing_date=now(),
            is_published=True,
        )
        article1.set_current_language(original_lang)
        article1.save()

        # Now try to create an article with the same title in every possible
        # language and every possible language contexts.
        for context_lang, _ in settings.LANGUAGES:
            with override(context_lang):
                for article_lang, _ in settings.LANGUAGES:
                    try:
                        article = Article(
                            author=author, owner=author.user,
                            app_config=self.app_config, publishing_date=now(),
                            is_published=True,
                        )
                        article.set_current_language(article_lang)
                        article.title = title
                        article.save()
                    except Exception:
                        self.fail('Creating article in process context "{}" '
                            'and article language "{}" with identical name '
                            'as another "{}" article raises exception'.format(
                                context_lang,
                                article_lang,
                                original_lang,
                            ))
