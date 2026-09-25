from django.contrib.auth import get_user_model
from django.test import TransactionTestCase, override_settings
from django.urls import reverse

from aldryn_people.models import Person

from aldryn_newsblog.cms_appconfig import NewsBlogConfig
from aldryn_newsblog.models import Article

from .mixins import NewsBlogTestCase, NewsBlogTestsMixin


class AdminTest(NewsBlogTestsMixin, TransactionTestCase):

    def test_admin_owner_default(self):
        from django.contrib import admin
        admin.autodiscover()
        # since we now have data migration to create the default
        # NewsBlogConfig (if migrations were not faked, django >1.7)
        # we need to delete one of configs to be sure that it is pre selected
        # in the admin view.
        if NewsBlogConfig.objects.count() > 1:
            # delete the app config that was created during test set up.
            NewsBlogConfig.objects.filter(namespace='NBNS').delete()
        user = self.create_user()
        user.is_superuser = True
        user.save()

        person = Person.objects.create(user=user, name=' '.join(
            (user.first_name, user.last_name)))

        admin_inst = admin.site._registry[Article]
        self.request = self.get_request('en')
        self.request.user = user
        self.request.META['HTTP_HOST'] = 'example.com'
        response = admin_inst.add_view(self.request)
        self.assertContains(response, f"""<option value="{user.pk}" selected>{user.username}</option>""", html=True)
        self.assertContains(response, f"""<option value="{person.pk}" selected>{user.get_full_name()}</option>""",
                            html=True)


class ArticleAdminTest(NewsBlogTestCase):

    def setUp(self):
        super().setUp()
        self.author = self.create_person()
        self.owner = self.author.user
        self.admin = get_user_model().objects.create(username="admin", is_staff=True, is_superuser=True)
        self.articles = self._create_articles()
        self.articles[0].related.add(self.articles[2])

    def _create_article(self, title: str, slug: str) -> None:
        return self.create_article(author=self.author, owner=self.owner, title=title, slug=slug)

    def _create_articles(self):
        articles = []
        for title, slug in (
            ("First page", "first-page"),
            ("Second page", "second-page"),
            ("Third page", "third-page",)
        ):
            articles.append(self._create_article(title, slug))
        return articles

    def test_article_change(self):
        self.client.force_login(self.admin)
        path = reverse("admin:aldryn_newsblog_article_change", kwargs={"object_id": self.articles[0].pk})
        response = self.client.get(path)
        self.assertNotContains(response, f"""
            <span id="fetch-related-articles" data-endpoint="/en/page/related-articles/{self.articles[0].pk}/"></span>
        """, html=True)
        self.assertContains(response, f"""
            <ul class="sortedm2m-items">
                <li class="sortedm2m-item">
                    <label for="id_related_0">
                        <input type="checkbox" name="related" value="{self.articles[2].pk}" id="id_related_0"
                            name="related" class="sortedm2m" checked> Third page</label>
                </li>
                <li class="sortedm2m-item">
                    <label for="id_related_1">
                        <input type="checkbox" name="related" value="{self.articles[1].pk}" id="id_related_1"
                            name="related" class="sortedm2m"> Second page</label>
                </li>
            </ul>""", html=True)

    @override_settings(ALDRYN_NEWSBLOG_FETCH_RELATED_ARTICLES=True)
    def test_article_change_js(self):
        self.client.force_login(self.admin)
        path = reverse("admin:aldryn_newsblog_article_change", kwargs={"object_id": self.articles[0].pk})
        response = self.client.get(path)
        self.assertContains(response, f"""
            <span id="fetch-related-articles" data-endpoint="/en/page/related-articles/{self.articles[0].pk}/"></span>
        """, html=True)
        self.assertContains(response, f"""
            <ul class="sortedm2m-items">
                <li class="sortedm2m-item">
                    <label for="id_related_0">
                        <input type="checkbox" name="related" value="{self.articles[2].pk}" id="id_related_0"
                            name="related" class="sortedm2m" checked> Third page</label>
                </li>
            </ul>""", html=True)

    def test_article_add(self):
        self.client.force_login(self.admin)
        path = reverse('admin:aldryn_newsblog_article_add') + f"?app_config={self.app_config.pk}"
        response = self.client.get(path)
        self.assertNotContains(response, f"""
            <span id="fetch-related-articles" data-endpoint="/en/page/related-articles/{self.articles[0].pk}/"></span>
        """, html=True)
        self.assertContains(response, f"""
            <ul class="sortedm2m-items">
                <li class="sortedm2m-item">
                    <label for="id_related_0">
                        <input type="checkbox" name="related" value="{self.articles[2].pk}" id="id_related_0"
                            name="related" class="sortedm2m"> Third page</label>
                </li>
                <li class="sortedm2m-item">
                    <label for="id_related_1">
                        <input type="checkbox" name="related" value="{self.articles[1].pk}" id="id_related_1"
                            name="related" class="sortedm2m"> Second page</label>
                </li>
                <li class="sortedm2m-item">
                    <label for="id_related_2">
                        <input type="checkbox" name="related" value="{self.articles[0].pk}" id="id_related_2"
                            name="related" class="sortedm2m"> First page</label>
                </li>
            </ul>""", html=True)

    @override_settings(ALDRYN_NEWSBLOG_FETCH_RELATED_ARTICLES=True)
    def test_article_add_js(self):
        self.client.force_login(self.admin)
        path = reverse('admin:aldryn_newsblog_article_add') + f"?app_config={self.app_config.pk}"
        response = self.client.get(path)
        self.assertContains(response, """
            <span id="fetch-related-articles" data-endpoint="/en/page/related-articles/add/NBNS/"></span>
        """, html=True)
        self.assertContains(response, """<ul class="sortedm2m-items"></ul>""", html=True)
