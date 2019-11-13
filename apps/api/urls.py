from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^activities/individual/$', views.IndividualActivitiesView.as_view(), name='individual-activities'),
    url(r'^activities/group/$', views.GroupActivityView.as_view(), name='group-activities'),
    url(r'^activities/nearby/$', views.NearbyActivitiesView.as_view(), name='nearby-activities'),
    url(r'^activities/(?P<uuid>\w+)/$', views.ActivityView.as_view(), name='activity'),
    url(r'^activities/(?P<uuid>\w+)/tags/$', views.ActivityTagsView.as_view(), name='activity-tags'),
    url(r'^activities/(?P<uuid>\w+)/address/$', views.RegisterActivityAddress.as_view(), name='activity-address'),

    url(r'^groups/$', views.UserGroupView.as_view(), name='user-groups'),
    url(r'^groups/(?P<uuid>\w+)/$', views.GroupView.as_view(), name='groups'),

    url(r'^user/activities/$', views.UserActivitiesView.as_view(), name='user-future-activities'),
    url(r'^user/address/$', views.UserAddressView.as_view(), name='user-address'),
]
