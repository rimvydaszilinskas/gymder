from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^activities/individual/$', views.IndividualActivitiesView.as_view(), name='individual-activities'),
    url(r'^activities/group/$', views.GroupActivityView.as_view(), name='group-activities'),
    url(r'^activities/(?P<uuid>\w+)/$', views.ActivityView.as_view(), name='activity'),
]
