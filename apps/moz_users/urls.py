from django.conf.urls import url
import views

urlpatterns = [
    url(r'^upload[/]$', views.upload, name='upload'),
]
