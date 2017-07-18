from django.core.urlresolvers import resolve
from django.test import TestCase

from .views import homepage


class SmokeTest(TestCase):
    def test_root_url_resolves_to_homepage(self):
        found = resolve('/')
        self.assertEqual(found.func, homepage)

    def test_homepage_returns_correct_HTML(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_homepage_can_save_post_request(self):
        response = self.client.post('/', {'item_text': 'new item list'})

        self.assertIn('new item list', response.content.decode())
