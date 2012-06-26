from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r"^login[/]", 'apps.site.views.login_view', name="login"),
    url(r'^user/', include('apps.moz_users.urls')),
    url(r'^$', 'apps.moz_users.views.upload'),
    url(r'^administration/', include('apps.moz_desktop.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
