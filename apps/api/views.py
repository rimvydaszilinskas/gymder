from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.activities.constants import ActivityFormat
from apps.activities.models import (
    Activity,
    GroupActivity,
    IndividualActivity
)
from apps.activities.serializers import (
    ActivitySerializer, 
    IndividualActivitySerializer,
    GroupActivitySerializer
)
from apps.activities.utils import can_edit_activity, can_view_activity
from apps.utils.models import Tag
from apps.utils.serializers import TagSerializer
from apps.utils.views_mixins import PutPatchMixin

from .views_mixins import FindActivityMixin, ActivityMixin


class IndividualActivitiesView(ActivityMixin, APIView):
    """
    Handle getting and creating individual activities
    """
    object_class = IndividualActivity
    serializer_class = IndividualActivitySerializer


class GroupActivityView(ActivityMixin, APIView):
    """
    Handle getting and creating group activities
    """
    object_class = GroupActivity
    serializer_class = GroupActivitySerializer


class ActivityView(PutPatchMixin, FindActivityMixin, APIView):
    """
    Individual and group activity UD
    """
    individual_serializer_class = IndividualActivitySerializer
    group_serializer_class = None

    def get(self, request, *args, **kwargs):
        activity = self.get_object(kwargs['uuid'])

        can_view_activity(activity, request.user, raise_exception=True)
        
        if activity.FORMAT == ActivityFormat.INDIVIDUAL:
            serializer = self.individual_serializer_class(activity)
        else:
            serializer = self.group_serializer_class(activity)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        activity = self.get_object(kwargs['uuid'])

        can_edit_activity(activity, request.user, raise_exception=True)

        if activity.FORMAT == ActivityFormat.INDIVIDUAL:
            serializer = self.individual_serializer_class(activity, data=request.data)
        else:
            serializer = self.group_serializer_class(activity, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data)

    def delete(self, request, *args, **kwargs):
        activity = self.get_object(kwargs['uuid'])

        can_edit_activity(activity, request.user, raise_exception=True)

        activity.is_deleted = True
        activity.save(update_fields=['is_deleted'])

        return Response(status=status.HTTP_200_OK)


class ActivityTagsView(APIView):
    serializer_class = TagSerializer

    def post(self, request, *args, **kwargs):
        uuid = kwargs['uuid']
        activity = get_object_or_404(Activity, uuid=uuid)

        can_edit_activity(activity, request.user, raise_exception=True)

        activity_tags = []
        activity.tags.clear()
        tags = request.data.get('tags', None)

        if tags and isinstance(tags, list):
            for tag in tags:
                title = tag.get('title', None)
                tag_uuid = tag.get('uuid', None)

                if tag_uuid:
                    tag_db, created = Tag.objects.get_or_create(uuid=tag_uuid)
                else:
                    tag_db, created = Tag.objects.get_or_create(title=title)

                activity.tags.add(tag_db)
                activity_tags.append(tag_db)
        
        serializer = self.serializer_class(activity_tags, many=True)

        return Response(status=status.HTTP_200_OK, data=serializer.data)
