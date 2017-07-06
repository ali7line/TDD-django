from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
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
        expected_html = render_to_string('home.html')

        self.assertEqual(response.content.decode(), expected_html)
