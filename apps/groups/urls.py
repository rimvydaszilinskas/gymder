from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.UserGroupsView.as_view(), name='index'),
    url(r'^create/$', views.CreateGroupView.as_view(), name='create'),
    url(r'^(?P<uuid>\w+)/$', views.GroupView.as_view(), name='preview'),
    url(r'^(?P<uuid>\w+)/members/$', views.GroupMembersView.as_view(), name='members'),
    url(r'^(?P<uuid>\w+)/activities/$', views.GroupActivitiesView.as_view(), name='activities'),
    url(r'^(?P<uuid>\w+)/activities/create/$', views.CreateActivityView.as_view(), name='create-activites'),
]
