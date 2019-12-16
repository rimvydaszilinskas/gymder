from datetime import datetime

from django.views import View
from django.shortcuts import get_object_or_404
from django.db.models import Q

from apps.activities.serializers import ActivitySerializer
from apps.activities.constants import RequestStatus
from apps.pages.views_mixins import PageViewMixin
from apps.users.serializers import UserSerializer
from apps.utils.models import Tag
from apps.utils.serializers import TagSerializer

from .models import (
    Activity, 
    GroupActivity, 
    IndividualActivity,
    Request
)
from .serializers import (
    IndividualActivitySerializer,
    GroupActivitySerializer,
    RequestSerializer
)
from .utils import can_view_activity


class ActivityView(PageViewMixin):
    """ Activity view """
    BUNDLE_NAME = 'activity_view'

    def create_js_context(self, request, *args, **kwargs):
        # capture the created tag. Might show more info on the first run
        created = request.GET.get('created', None)

        activity = get_object_or_404(Activity, uuid=kwargs['uuid'])

        can_view_activity(activity, request.user, raise_exception=True)

        # try getting user reuqest
        try:
            # user_request = Request.objects.get(user=request.user, is_deleted=False)
            user_request = activity.requests.get(user=request.user, is_deleted=False)
            user_request = RequestSerializer(user_request).data
        except:
            user_request = None

        if activity.is_group:
            activity = get_object_or_404(GroupActivity, uuid=activity.uuid)
            serializer = GroupActivitySerializer(activity)
        else:
            activity = get_object_or_404(IndividualActivity, uuid=activity.uuid)
            serializer = IndividualActivitySerializer(activity)

        user = request.user
        user_serializer = UserSerializer(user)

        return {
            'user': user_serializer.data,
            'activity': serializer.data,
            'created': created == 'true',
            'is_owner': activity.user == user,
            'user_request': user_request
        }


class ActivityAttendeeView(ActivityView):
    BUNDLE_NAME = 'activity_attendees'


class CreateActivityView(PageViewMixin):
    """ Create activities """
    BUNDLE_NAME = 'create_activity'

    def create_js_context(self, request, *args, **kwargs):
        # Return user data as JSON to the JS view
        user = request.user

        serializer = UserSerializer(user)

        return {
            'user': serializer.data
        }


class ActivitiesView(PageViewMixin):
    BUNDLE_NAME = 'activities_view'
    TITLE = 'Activities'

    def create_js_context(self, request, *args, **kwargs):
        activities = Activity.objects.filter(
            Q(user=request.user) | Q(
                requests__user=request.user,
                requests__status=RequestStatus.APPROVED,
                requests__is_deleted=False
            ),
            is_deleted=False
        )

        all_activities = activities.filter(time__gte=datetime.today()).order_by('-time')
        
        past_activities = activities.filter(time__lt=datetime.today()).order_by('-time')

        owned_activities = Activity.objects.filter(
            is_deleted=False,
            time__gte=datetime.today(),
            user=request.user).order_by('-time')

        serializer = ActivitySerializer(all_activities, many=True)
        owned_activities_serializer = ActivitySerializer(owned_activities, many=True)
        past_activities_serializer = ActivitySerializer(past_activities, many=True)

        return {
            'activities': serializer.data,
            'owned_activities': owned_activities_serializer.data,
            'past_activities': past_activities_serializer.data
        }


class SearchActivitiesView(PageViewMixin):
    BUNDLE_NAME = 'activities_search'
    TITLE = 'Search activities'


class TagFilterView(PageViewMixin):
    BUNDLE_NAME = 'activity_tag_filtering'
    serializer_class = ActivitySerializer

    def create_js_context(self, request, *args, **kwargs):
        tag = get_object_or_404(Tag, uuid=kwargs['uuid'])

        activities = Activity.objects.filter(
            Q(user=request.user) | Q(public=True) |
            Q(
                requests__user=request.user,
                requests__status=RequestStatus.APPROVED,
                requests__is_deleted=False
            ),
            is_deleted=False,
            tags=tag
        ).filter(time__gte=datetime.today()).order_by('-time')

        serializer = self.serializer_class(activities, many=True)
        tag_serializer = TagSerializer(tag)

        return {
            'activities': serializer.data,
            'tag': tag_serializer.data
        }
