from django.conf.urls import url, include
from django.contrib import admin

from lists.views import homepage
import lists.urls as lists_urls

urlpatterns = [
        url(r'^$', homepage, name='root'),
        url('^lists/', include(lists_urls, namespace='lists')),
        url(r'^admin/', admin.site.urls),
]
