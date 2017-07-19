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

    def test_homepage_can_save_POST_request(self):
        self.client.post('/', {'item_text': 'new item list'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'new item list')

    def test_homepage_redirects_after_POST_request(self):
        response = self.client.post('/', {'item_text': 'new item list'})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/the-only-list/')

    def test_homepage_save_item_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list/')
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_display_all_items(self):
        Item.objects.create(text='first item in list')
        Item.objects.create(text='second item in list')

        response = self.client.get('/lists/the-only-list/')

        self.assertContains(response, 'first item in list')
        self.assertContains(response, 'second item in list')


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
