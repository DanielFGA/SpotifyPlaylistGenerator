from django.conf.urls import url
from django.urls import path

from PlaylistGenerator import views

urlpatterns = [
    path('start', views.start, name='start'),
    path('start/auth', views.auth_start, name='start_auth'),
    url(regex=r'^select/$', view=views.authorizes_access),
    path('select/go', views.generate_playlist, name='generate_playlist'),
]