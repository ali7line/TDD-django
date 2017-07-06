from django.conf.urls import url
from django.contrib import admin

from lists.views import homepage

urlpatterns = [
        url(r'^$', homepage, name='root'),
        url(r'^admin/', admin.site.urls),
]
