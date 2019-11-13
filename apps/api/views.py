from datetime import datetime

from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView

from apps.activities.constants import ActivityFormat, RequestStatus
from apps.activities.models import (
    Activity,
    GroupActivity,
    IndividualActivity
)
from apps.activities.serializers import (
    ActivitySerializer, 
    IndividualActivitySerializer,
    GroupActivitySerializer,
    RequestSerializer,
    UserRequestSerializer
)
from apps.activities.utils import can_edit_activity, can_view_activity, find_close_to_address
from apps.utils.models import Tag
from apps.utils.serializers import (
    TagSerializer,
    AddressSerializer,
    MinimalAddressSerializer
)
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


class UserActivitiesView(ListAPIView):
    """ Get future user activities """
    serializer_class = ActivitySerializer

    def get_queryset(self):
        return Activity.objects.filter(
            time_gte=datetime.today(),
            is_deleted=False
        ).filter(
            Q(user=self.request.user) | Q(
                requests__user=self.request.user,
                requests__status=RequestStatus.APPROVED
            )
        )


class RegisterActivityAddress(FindActivityMixin, APIView):
    """
    Activity address API endpoint
    """
    serializer_class = AddressSerializer

    def get(self, request, *args, **kwargs):
        activity = self.get_object(kwargs['uuid'])

        serializer = self.serializer_class(activity.address)

        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def post(self, request, *args, **kwargs):
        activity = self.get_object(kwargs['uuid'])

        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        address_instance = serializer.save()

        address_instance.user = request.user
        address_instance.save(update_fields=['user'])

        activity.address = address_instance
        activity.save(update_fields=['address'])

        return Response(status=status.HTTP_201_CREATED, data=serializer.data)


class NearbyActivitiesView(APIView):
    address_serializer_class = MinimalAddressSerializer
    serializer_class = ActivitySerializer

    def get(self, request, *args, **kwargs):
        address_serializer = self.address_serializer_class(data=request.data)

        address_serializer.is_valid(raise_exception=True)
        address_instance = address_serializer.save()

        address_instance.user = request.user
        address_instance.save(update_fields=['user'])

        activities = find_close_to_address(address_instance)

        serializer = self.serializer_class(activities, many=True)

        if len(activities) != 0:
            return Response(status=status.HTTP_200_OK, data=serializer.data)

        return Response(status=status.HTTP_404_NOT_FOUND)


class UserAddressView(APIView):
    """
    CRUD user address
    """
    serializer_class = AddressSerializer

    def get(self, request, *args, **kwargs):
        address = request.user.address

        serializer = self.serializer_class(address)

        return Response(
            data=serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        instance = serializer.save()

        user = request.user

        user.address = instance
        user.save(update_fields=['address'])

        instance.user = user
        instance.save(update_fields=['user'])

        return Response(
            status=status.HTTP_201_CREATED, 
            data=serializer.data)
