from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^activities/$', views.ActivitiesView.as_view(), name='activities'),
    url(r'^activities/(?P<uuid>\w+)/$', views.ActivityView.as_view(), name='activity'),
]
