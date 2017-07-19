from django.conf.urls import url
from django.contrib import admin

from lists.views import homepage, view_list, new_list

urlpatterns = [
        url(r'^$', homepage, name='root'),
        url(r'^lists/(?P<list_id>\d+)/$', view_list, name='view_list'),
        url('^lists/new$', new_list, name='new_list'),
        url(r'^admin/', admin.site.urls),
]
