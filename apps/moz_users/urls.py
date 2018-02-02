from django.conf.urls import url, include
import views

urlpatterns = [
    url(r'^upload[/]$', views.upload, name='upload'),
]
