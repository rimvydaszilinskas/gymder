from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.activities.models import (
    Activity,
    GroupActivity,
    IndividualActivity
)
from apps.activities.serializers import ActivitySerializer
from apps.utils.views_mixins import PutPatchMixin


class ActivitiesView(APIView):
    serializer_class = ActivitySerializer

    def get(self, request, *args, **kwargs):
        activities = Activity.objects.all()

        serializer = self.serializer_class(activities, many=True)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            status=status.HTTP_201_CREATED,
            data=serializer.data)


class ActivityView(PutPatchMixin, APIView):
    serializer_class = ActivitySerializer

    def get(self, request, *args, **kwargs):
        activity = get_object_or_404(Activity, uuid=kwargs['uuid'])

        serializer = self.serializer_class(activity)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        activity = get_object_or_404(Activity, uuid=kwargs['uuid'])

        serializer = self.serializer_class(activity, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data)
