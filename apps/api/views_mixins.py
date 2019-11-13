from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import status

from apps.activities.constants import RequestStatus
from apps.activities.models import GroupActivity, IndividualActivity
from apps.groups.constants import MembershipTypes
from apps.groups.models import Group, Membership


class FindActivityMixin(object):
    """
    Mixin to help find the activity based on UUID.
    """

    def get_object(self, uuid, data=None):
        """
        Finds appropriate activity and returns a tuple of object and serializer
        """
        try:
            activity = IndividualActivity.objects.get(uuid=uuid, is_deleted=False)
        except:
            activity = get_object_or_404(GroupActivity, uuid=uuid, is_deleted=False)

        return activity


class ActivityMixin(object):
    """
    General view for getting activities

    Specify `object_class` and `serializer_class` to use this
    """
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


class GroupMixin(object):
    def get_group(self, uuid, user):
        group = get_object_or_404(Group, uuid=uuid, is_deleted=False)

        membership = group.memberships.filter(user=user, status=RequestStatus.APPROVED)
        
        if membership.exists() or \
            group.user==user or \
                (group.public==True and group.needs_approval==False ):
            
            return group

        raise HttpResponseForbidden()

    def get_group_edit(self, uuid, user):
        group = self.get_group(uuid, user)

        membership = group.memberships.filter(user=user, status=RequestStatus.APPROVED)

        if group.user == user:
            return group

        if membership.exists():
            membership = membership.first()

            if membership.membership_type == MembershipTypes.ADMIN:
                return group

        raise HttpResponseForbidden()
