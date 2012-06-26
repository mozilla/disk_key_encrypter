from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    url(r'^upload[/]$', views.upload, name='upload'),
)
