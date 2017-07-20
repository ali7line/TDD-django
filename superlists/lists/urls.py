from django.conf.urls import url

from .views import view_list, new_list, add_item

urlpatterns = [
        url(r'^(?P<list_id>\d+)/$', view_list, name='view_list'),
        url(r'^(?P<list_id>\d+)/add_item$', add_item, name='add_item'),
        url('^new$', new_list, name='new_list'),
]
