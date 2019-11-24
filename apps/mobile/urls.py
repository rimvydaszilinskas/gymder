from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.PingView.as_view(), name='ping'),
    url(r'^auth/$', views.AuthPingView.as_view(), name='authentication-ping'),
    url(r'^login/$', views.AuthenticateUserView.as_view(), name='login'),
]

