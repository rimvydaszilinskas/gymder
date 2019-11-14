from django.conf.urls import url

from . import views

urlpatterns = [
    # Activities paths
    url(r'^activities/individual/$', views.IndividualActivitiesView.as_view(), name='individual-activities'),
    url(r'^activities/group/$', views.GroupActivityView.as_view(), name='group-activities'),
    url(r'^activities/nearby/$', views.NearbyActivitiesView.as_view(), name='nearby-activities'),
    url(r'^activities/(?P<uuid>\w+)/$', views.ActivityView.as_view(), name='activity'),
    url(r'^activities/(?P<uuid>\w+)/tags/$', views.ActivityTagsView.as_view(), name='activity-tags'),
    url(r'^activities/(?P<uuid>\w+)/address/$', views.RegisterActivityAddress.as_view(), name='activity-address'),
    url(r'^activities/(?P<uuid>\w+)/posts/$', views.ActivityPostView.as_view(), name='activity-posts'),
    url(r'^activities/(?P<uuid>\w+)/requests/$', views.ActivityRequestView.as_view(), name='activity-requests'),
    url(r'^activities/(?P<uuid>\w+)/requests/(?P<request_uuid>\w+)/$', views.RequestView.as_view(), name='requests'),
    # Communications paths
    url(r'^communication/post/(?P<uuid>\w+)/$', views.PostView.as_view(), name='posts'),
    url(r'^communication/post/(?P<uuid>\w+)/comments/$', views.CommentView.as_view(), name='add-comment'),
    url(r'^communication/post/(?P<uuid>\w+)/comments/(?P<comment_uuid>\w+)/$',
        views.CommentView.as_view(), name='delete-comment'),

    # Membership paths
    url(r'^memberships/(?P<uuid>\w+)/$', views.MembershipView.as_view(), name='memberships'),

    # Group paths
    url(r'^groups/$', views.UserGroupView.as_view(), name='user-groups'),
    url(r'^groups/(?P<uuid>\w+)/$', views.GroupView.as_view(), name='groups'),
    url(r'^groups/(?P<uuid>\w+)/memberships/$', views.GroupMembershipsView.as_view(), name='groups-memberships'),
    url(r'^groups/(?P<uuid>\w+)/posts/$', views.GroupPostView.as_view(), name='group-posts'),

    # User paths
    url(r'^user/activities/$', views.UserActivitiesView.as_view(), name='user-future-activities'),
    url(r'^user/address/$', views.UserAddressView.as_view(), name='user-address'),
    url(r'^user/memberships/$', views.UserMembershipsView.as_view(), name='user-memberships'),

]
