from django.conf.urls import url

from . import views

from apps.api import views as api_views


urlpatterns = [
    url(r'^$', views.PingView.as_view(), name='ping'),
    url(r'^auth/$', views.AuthPingView.as_view(), name='authentication-ping'),
    url(r'^login/$', views.AuthenticateUserView.as_view(), name='login'),

    url(r'^activities/$', api_views.UserActivitiesView.as_view(), name='user-activities'),
    url(r'^activities/(?P<uuid>\w+)/$', api_views.ActivityView.as_view(), name='activity-view'),
    url(r'^activities/(?P<uuid>\w+)/posts/$', api_views.ActivityPostView.as_view(), name='activity-posts'),
]
