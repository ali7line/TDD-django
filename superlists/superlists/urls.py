from django.conf.urls import url
from django.contrib import admin

from lists.views import homepage, view_list

urlpatterns = [
        url(r'^lists/the-only-list/$', view_list, name='view_list'),
        url(r'^$', homepage, name='root'),
        url(r'^admin/', admin.site.urls),
]
