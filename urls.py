from django.conf.urls import url, include
from django.contrib import admin
from apps.site.views import login_view
from apps.moz_users.views import upload, index_upload
from django.conf import settings
import os
admin.autodiscover()
ALLOW_ADMIN = False

# URLs accessible on any Django instance
urlpatterns = [
    url(r'^user/', include('apps.moz_users.urls')),
    url(r"^login[/]", login_view, name="login"),
    url(r'^$', index_upload, name="index_upload"),
    url(r'^administration/', include('apps.moz_desktop.urls'), name='administration'),
    url(r'^admin/', admin.site.urls),
]