from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    # url(r'^ready$', views.ready),

    url(r'^game/(?P<content>\w*)$', views.game),
    url(r'^append/(?P<content>\w*)/?', views.append),
    url(r'^delete/(?P<content>\w*)/?(?P<res_id>\w*)/?', views.delete),
    url(r'^detail/(?P<content>\w*)/?(?P<res_id>\w*)/?(?P<name>\w*)$', views.detail),
    url(r'^user/(?P<content>\w+)$', views.user),
    url(r'^admin_check$', views.admin),
]
