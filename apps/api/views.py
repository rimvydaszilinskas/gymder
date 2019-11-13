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
from apps.groups.constants import MembershipTypes
from apps.groups.models import Group, Membership
from apps.groups.serializer import (
    GroupSerializer,
    MembershipSerializer,
    UserMembershipSerializer
)
from apps.users.models import User
from apps.utils.models import Tag
from apps.utils.serializers import (
    TagSerializer,
    AddressSerializer,
    MinimalAddressSerializer
)
from apps.utils.views_mixins import PutPatchMixin

from .views_mixins import (
    FindActivityMixin,
    ActivityMixin,
    GroupMixin,
    MembershipMixin
)


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
    """
    View for adding tags to activity
    """
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


class UserMembershipsView(ListAPIView):
    """
    Retrieve all user group memberships
    """
    serializer_class = UserMembershipSerializer

    def get_queryset(self):
        return self.request.user.memberships.filter(
            is_deleted=False, status=RequestStatus.APPROVED)


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


class UserGroupView(ListAPIView):
    """
    User group view
    """
    serializer_class = GroupSerializer

    def get_queryset(self):
        groups = Group.objects.filter(
            is_deleted=False).filter(
                Q(user=self.request.user) | Q(
                    memberships__user=self.request.user, 
                    memberships__status=RequestStatus.APPROVED)
            )
        
        return groups

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        group = serializer.save(user=request.user)

        Membership.objects.create(
            group=group,
            user=request.user,
            membership_type=MembershipTypes.ADMIN,
            status=RequestStatus.APPROVED)

        return Response(
            status=status.HTTP_201_CREATED, 
            data=serializer.data)


class GroupView(GroupMixin, PutPatchMixin, APIView):
    """
    User group view
    """
    serializer_class = GroupSerializer

    def get(self, request, *args, **kwargs):
        group = self.get_group(uuid=kwargs['uuid'], user=request.user)

        serializer = self.serializer_class(group)

        return Response(data=serializer.data)

    def post(self, request, *args, **kwargs):
        group = self.get_group_edit(uuid=kwargs['uuid'], user=request.user)

        serializer = self.serializer_class(group, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data)

    def delete(self, request, *args, **kwargs):
        group = self.get_group(uuid=kwargs['uuid'], user=request.user)
        
        if group.user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        group.is_deleted = True
        group.save(update_fields=['is_deleted'])

        return Response(status=status.HTTP_200_OK)


class GroupMembershipsView(GroupMixin, APIView):
    """
    Base group membership view for previewing memberships and adding new ones
    """
    serializer_class = MembershipSerializer

    def get(self, request, *args, **kwargs):
        group = self.get_group(kwargs['uuid'], request.user)

        serializer = self.serializer_class(
            group.memberships.filter(is_deleted=False), many=True)
        
        return Response(data=serializer.data)

    def post(self, request, *args, **kwargs):
        group = self.get_group(uuid=kwargs['uuid'], user=request.user)

        user_uuid = request.data.get('user_uuid', None)
        user_email = request.data.get('user_email', None)
        membership_status = RequestStatus.APPROVED if not group.needs_approval else RequestStatus.PENDING

        if user_uuid:
            user = get_object_or_404(User, uuid=user_uuid)
        elif user_email:
            user = get_object_or_404(User, email=user_email)
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST, 
                data={'detail': 'please specify user_uuid'})

        membership = Membership.objects.create(
            user=user,
            group=group,
            status=membership_status,
            membership_type=MembershipTypes.PARTICIPANT)

        serializer = self.serializer_class(membership)

        return Response(
            status=status.HTTP_201_CREATED,
            data=serializer.data)


class MembershipView(MembershipMixin, APIView):
    """
    View for managing specific memberships
    """
    serializer_class = MembershipSerializer

    def get(self, request, *args, **kwargs):
        """
        This returns the specified membership

        The rules for who can see it are defined in get_membership from MembershipMixin
        """
        membership = self.get_membership(
            uuid=kwargs['uuid'],
            user=request.user)
        
        serializer = self.serializer_class(membership)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """
        Edit membership

        Only the superuser and group admin/owner can access this
        """
        membership = self.get_membership_edit(
            uuid=kwargs['uuid'], user=request.user)

        serializer = self.serializer_class(membership, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def delete(self, request, *args, **kwargs):
        """
        Delete membership

        Can be accessed by superuser, group admin and the user of the membership
        """
        membership = self.get_membership_delete(kwargs['uuid'], user=request.user)

        membership.is_deleted = True
        membership.save(update_fields=['is_deleted'])

        return Response(status=status.HTTP_200_OK)
