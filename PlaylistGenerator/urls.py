from django.conf.urls import url
from django.urls import path

from PlaylistGenerator import views

urlpatterns = [
    path('start', views.start, name='start'),
    #url(r'127.0.0.1:8000\/generator\/start\/authorizes_access\?code=[0-9a-zA-Z]*&state=[0-9a-zA-Z]*', views.authorizes_access, name='authorizes_access'),
    url(regex=r'^start/authorizes_access/$', view=views.authorizes_access),
    #url("start", view=views.start),
    path('start/auth', views.auth_start, name='start_auth'),
]