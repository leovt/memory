from django.conf.urls import url

from . import views

app_name = 'memory'
urlpatterns = [
    url(r'^$', views.welcome, name='welcome'),
    url(r'^(?P<urlid>[0-9a-z]+)/$', views.game, name='game'),
]
