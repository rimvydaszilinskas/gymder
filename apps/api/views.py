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
from apps.utils.views_mixins import PutPatchMixin

from .views_mixins import FindActivityMixin, ActivityMixin


class IndividualActivitiesView(ActivityMixin, APIView):
    """
    Handle creation of getting and creating activities
    """
    object_class = IndividualActivity
    serializer_class = IndividualActivitySerializer


class GroupActivityView(ActivityMixin, APIView):
    object_class = GroupActivity
    serializer_class = GroupActivitySerializer


class ActivityView(PutPatchMixin, FindActivityMixin, APIView):
    """
    Individual and group activity CRUD
    """
    individual_serializer_class = IndividualActivitySerializer
    group_serializer_class = None

    def get(self, request, *args, **kwargs):
        activity = self.get_object_and_serializer(kwargs['uuid'])
        
        if activity.FORMAT == ActivityFormat.INDIVIDUAL:
            serializer = self.individual_serializer_class(activity)
        elif activity.FORMAT == ActivityFormat.GROUP:
            serializer = self.group_serializer_class(activity)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        activity = self.get_object_and_serializer(kwargs['uuid'])

        if activity.FORMAT == ActivityFormat.INDIVIDUAL:
            serializer = self.individual_serializer_class(activity, data=request.data)
        elif activity.FORMAT == ActivityFormat.GROUP:
            serializer = self.group_serializer_class(activity, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data)
