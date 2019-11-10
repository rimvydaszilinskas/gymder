from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import status

from apps.activities.models import GroupActivity, IndividualActivity


class FindActivityMixin(object):
    """
    Mixin to help find the activity based on UUID.
    """

    def get_object_and_serializer(self, uuid, data=None):
        """
        Finds appropriate activity and returns a tuple of object and serializer
        """
        try:
            activity = IndividualActivity.objects.get(uuid=uuid)
        except:
            activity = get_object_or_404(GroupActivity, uuid=uuid)

        return activity


class ActivityMixin(object):
    object_class = None
    serializer_class = None

    def get(self, request, *args, **kwargs):
        activities = self.object_class.objects.all()

        serializer = self.serializer_class(activities, many=True)

        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid()
        instance = serializer.save(user=request.user)

        serializer = self.serializer_class(instance)

        return Response(
            status=status.HTTP_201_CREATED,
            data=serializer.data)
