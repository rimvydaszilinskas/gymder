from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^create/$', views.CreateActivityView.as_view(), name='create-activity'),
    url(r'^(?P<uuid>\w+)/$', views.ActivityView.as_view(), name='preview'),
    url(r'^(?P<uuid>\w+)/attendees/$', views.ActivityAttendeeView.as_view(), name='attendees'),
    
]