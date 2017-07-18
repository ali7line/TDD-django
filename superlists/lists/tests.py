from django.core.urlresolvers import resolve
from django.test import TestCase

from .views import homepage
from .models import Item


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


class ItemListTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'the first item in list'
        first_item.save()

        second_item = Item()
        second_item.text = 'the second item in list'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(Item.objects.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEqual(first_saved_item.text, 'the first item in list')
        self.assertEqual(second_saved_item.text, 'the second item in list')
