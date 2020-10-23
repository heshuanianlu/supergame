from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^client$', views.connect),
    # url(r'^room/(?P<username>\w+)$', views.room),
]
