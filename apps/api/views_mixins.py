from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import status

from apps.activities.constants import RequestStatus
from apps.activities.models import GroupActivity, IndividualActivity
from apps.communication.models import Post
from apps.groups.constants import MembershipTypes
from apps.groups.models import Group, Membership
from apps.utils.models import Address


class FindActivityMixin(object):
    """
    Mixin to help find the activity based on UUID.
    """

    def get_activity(self, uuid, user):
        """
        Finds appropriate activity and returns activity if user has enough rights
        """
        try:
            activity = IndividualActivity.objects.get(uuid=uuid, is_deleted=False)
        except:
            activity = get_object_or_404(GroupActivity, uuid=uuid, is_deleted=False)

        if activity.public:
            return activity
        
        if activity.user == user:
            return activity

        request = activity.requests.filter(
            user=user,
            is_deleted=False,
            status__in=[RequestStatus.PENDING, RequestStatus.APPROVED])

        if request.exists():
            return activity

        group = activity.group

        if group is not None:
            if group.user == user:
                return activity
            
            membership = group.memberships.filter(
                user=user, 
                status=RequestStatus.APPROVED, 
                is_deleted=False)

            if membership.exists():
                return activity

        raise PermissionDenied()


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

        serializer.is_valid(raise_exception=True)
        instance = serializer.save(user=request.user)

        # check if address uuid is attached
        if 'address_uuid' in request.data:
            try:
                address = Address.objects.get(uuid=request.data['address_uuid'])

                # attach the "creator" of the address
                address.user = request.user
                address.save(update_fields=['user'])

                instance.address = address
                instance.save(update_fields=['address'])
            except Exception as e:
                pass

        serializer = self.serializer_class(instance)

        return Response(
            status=status.HTTP_201_CREATED,
            data=serializer.data)


class GroupMixin(object):
    """
    Group mixin for retrieving groups based on rights

    Use `get_group` for preview

    Use `get_group_edit` for updating/deleting it
    """
    def get_group(self, uuid, user):
        group = get_object_or_404(Group, uuid=uuid, is_deleted=False)

        membership = group.memberships.filter(user=user, status=RequestStatus.APPROVED)
        
        if membership.exists() or \
            group.user==user or \
                (group.public==True and group.needs_approval==False ):
            
            return group

        raise PermissionDenied()

    def get_group_edit(self, uuid, user):
        group = self.get_group(uuid, user)

        membership = group.memberships.filter(user=user, status=RequestStatus.APPROVED)

        if group.user == user:
            return group

        if membership.exists():
            membership = membership.first()

            if membership.membership_type == MembershipTypes.ADMIN:
                return group

        raise PermissionDenied()


class MembershipMixin(object):
    """
    Membership mixin

    Use `get_membership` if it is for previewing it.
    Can be accessed by anyone in the group and the membership user

    Use `get_membership_edit` if it is for editing its status
    Can be accessed by group admins

    Use `get_membership_delete` if it for removing it
    Can be accessed by group admins and the membership user
    """
    def get_membership(self, uuid, user):
        membership = get_object_or_404(Membership, uuid=uuid, is_deleted=False)

        if membership.user == user:
            return membership

        group = membership.group

        if group.public:
            return membership

        group_membership = group.memberships.filter(
            user=user, 
            is_deletef=False, 
            status=RequestStatus.APPROVED)

        if group_membership.exists():
            return membership
        
        raise PermissionDenied()

    def get_membership_edit(self, uuid, user):
        membership = self.get_membership(uuid, user)
        group = membership.group

        if membership.group.user == user:
            return membership
        else:
            group_membership = group.memberships.filter(
                user=user, is_deleted=False, status=RequestStatus.APPROVED)

            if group_membership.exists() and \
                group_membership.membership_type == MembershipTypes.ADMIN:
                return membership
        
        raise PermissionDenied()

    def get_membership_delete(self, uuid, user):
        membership = self.get_membership(uuid, user)

        if membership.group.user == user or membership.user:
            return membership
        else:
            group_membership = membership.group.memberships.filter(
                user=user, is_deleted=False, status=RequestStatus.APPROVED)

            if group_membership.exists() and \
                group_membership.membership_type == MembershipTypes.ADMIN:
                return membership

        raise PermissionDenied()


class PostMixin(object):
    """
    Post mixin for retrieving posts
    """
    def get_post(self, uuid, user):
        post = get_object_or_404(Post, uuid=uuid, is_deleted=False)

        group = post.group
        activity = post.activity

        if post.user != user:
            if group is not None:
                membership = group.memberships.filter(
                    user=user,
                    is_deleted=False,
                    status=RequestStatus.APPROVED)
                
                if not membership.exists() and group.user != user:
                    raise PermissionDenied()
            elif activity is not None:
                if not activity.public:
                    activity_group = activity.group
                    
                    if activity_group is not None:
                        memberships = activity_group.memberships.filter(
                            user=user,
                            is_deleted=False,
                            status=RequestStatus.APPROVED)
                        
                        if not membership.exists() and activity_group != user:
                            raise PermissionDenied()
                    elif activity.user != user and \
                        not activity.requests.filter(
                            user=user, 
                            status__in=[RequestStatus.APPROVED, RequestStatus.PENDING], 
                            is_deleted=False).exists():
                        raise PermissionDenied()

        return post
    
    def get_post_delete(self, uuid, user):
        post = get_object_or_404(Post, uuid=uuid, is_deleted=False)

        group = post.group
        activity = post.activity

        if post.user == user:
            if group is not None:
                membership = group.memberships.filter(
                    user=user,
                    is_deleted=False,
                    status=RequestStatus.APPROVED,
                    membership_type=MembershipTypes.ADMIN)
                
                if not membership.exists() and group.user != user:
                    raise PermissionDenied()
            elif activity is not None:
                if activity.user != user:
                    activity_group = activity.group

                    if activity_group is not None:
                        memberships = activity_group.memberships.filter(
                            user=user,
                            is_deleted=False,
                            status=RequestStatus.APPROVED,
                            membership_type=MembershipTypes.ADMIN)
                        
                        if not memberships.exists() and activity_group.user != user:
                            raise PermissionDenied()
        return post
