from django.views import View
from django.shortcuts import get_object_or_404

from apps.pages.views_mixins import PageViewMixin
from apps.users.serializers import UserSerializer

from .models import Activity, GroupActivity, IndividualActivity
from .serializers import IndividualActivitySerializer, GroupActivitySerializer
from .utils import can_view_activity


class ActivityView(PageViewMixin):
    BUNDLE_NAME = 'view_activity'

    def create_js_context(self, request, *args, **kwargs):
        activity = get_object_or_404(Activity, uuid=kwargs['uuid'])

        can_view_activity(activity, request.user, raise_exception=True)

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
            'activity': serializer.data
        }


class CreateActivityView(PageViewMixin):
    BUNDLE_NAME = 'create_activity'

    def create_js_context(self, request, *args, **kwargs):
        # Return user data as JSON to the JS view
        user = request.user

        serializer = UserSerializer(user)

        return {'user': serializer.data}
