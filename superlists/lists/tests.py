from django.core.urlresolvers import resolve
from django.test import TestCase

from .views import homepage


class SmokeTest(TestCase):
    def test_root_url_resolves_to_homepage(self):
        found = resolve('/')
        self.assertEqual(found.func, homepage)
