from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.desktop_admin, name='desktop_admin'),
    url(r'^attach/(?P<filename>.+)$', views.download_attach, name='attach'),
    url(r'^detail/(?P<id_value>.+)$', views.detail, name='detail'),
    url(r'^upload[/]$', views.upload, name='desktop_admin_upload'),
]
