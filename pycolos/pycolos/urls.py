from django.conf.urls import url

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', auth_views.login, name='login'),
    url(r'^logout$', views.logout_view, name='logout'),
    url(r'^create_user$', views.newuser, name='create_user'),
]