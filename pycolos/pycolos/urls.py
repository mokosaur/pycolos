from django.conf.urls import url

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', auth_views.login, name='login'),
    url(r'^logout$', auth_views.logout, {'next_page': 'index'}, name='logout'),
    url(r'^create_user$', views.newuser, name='create_user'),
    url(r'^usos_users$', views.create_users_with_csv, name='usos_users'),
]
