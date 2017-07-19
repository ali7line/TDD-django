from django.core.urlresolvers import resolve
from django.test import TestCase

from .views import homepage
from .models import Item, List


class HomepageTest(TestCase):
    def test_root_url_resolves_to_homepage(self):
        found = resolve('/')
        self.assertEqual(found.func, homepage)

    def test_returns_correct_HTML(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_display_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='first item in list', list=correct_list)
        Item.objects.create(text='second item in list', list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='first item in other list', list=other_list)
        Item.objects.create(text='second item in other list', list=other_list)

        response = self.client.get('/lists/%d/' % (correct_list.id,))

        self.assertContains(response, 'first item in list')
        self.assertContains(response, 'second item in list')
        self.assertNotContains(response, 'other')


class NewListTest(TestCase):
    def test_saving_POST_request(self):
        self.client.post('/lists/new', {'item_text': 'new item list'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'new item list')

    def test_redirects_after_POST_request(self):
        response = self.client.post('/lists/new', {'item_text': 'new item list'})

        list_ = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % (list_.id,))


class ListAndItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'the first item in list'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'the second item in list'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(Item.objects.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEqual(first_saved_item.text, 'the first item in list')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'the second item in list')
        self.assertEqual(second_saved_item.list, list_)
