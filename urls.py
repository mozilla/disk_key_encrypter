from django.conf.urls import url, include
from django.contrib import admin
admin.autodiscover()
import apps.site.views as app_view
from apps.site.views import login_view
from apps.moz_users.views import upload

urlpatterns = [
    url(r'^user/', include('apps.moz_users.urls')),
    url(r"^login[/]", login_view, name="login"),
    url(r'^$', upload),
    url(r'^administration/', include('apps.moz_desktop.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
