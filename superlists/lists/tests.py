from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest

from .views import homepage


class SmokeTest(TestCase):
    def test_root_url_resolves_to_homepage(self):
        found = resolve('/')
        self.assertEqual(found.func, homepage)

    def test_homepage_returns_correct_HTML(self):
        request = HttpRequest()
        response = homepage(request)

        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>To-Do List</title>', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))
