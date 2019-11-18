from datetime import datetime

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponseForbidden

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView

from apps.activities.constants import ActivityFormat, RequestStatus
from apps.activities.models import (
    Activity,
    GroupActivity,
    IndividualActivity,
    Request
)
from apps.activities.serializers import (
    ActivitySerializer, 
    IndividualActivitySerializer,
    GroupActivitySerializer,
    RequestSerializer,
    UserRequestSerializer
)
from apps.activities.utils import can_edit_activity, can_view_activity, find_close_to_address
from apps.communication.models import Post, Comment
from apps.communication.serializers import (
    CommentSerializer, 
    PostSerializer,
    FullPostSerializer)  
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
    MembershipMixin,
    PostMixin
)

# Activities views


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
        activity = self.get_activity(kwargs['uuid'])

        can_view_activity(activity, request.user, raise_exception=True)
        
        if activity.FORMAT == ActivityFormat.INDIVIDUAL:
            serializer = self.individual_serializer_class(activity)
        else:
            serializer = self.group_serializer_class(activity)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        activity = self.get_activity(kwargs['uuid'])

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
                    if title is None:
                        continue

                    title = str(title)
                    tag_db, created = Tag.objects.get_or_create(title=title)

                activity.tags.add(tag_db)
                activity_tags.append(tag_db)
        
        serializer = self.serializer_class(activity_tags, many=True)

        return Response(status=status.HTTP_200_OK, data=serializer.data)


class RegisterActivityAddress(FindActivityMixin, APIView):
    """
    Activity address API endpoint
    """
    serializer_class = AddressSerializer

    def get(self, request, *args, **kwargs):
        activity = self.get_activity(kwargs['uuid'])

        serializer = self.serializer_class(activity.address)

        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def post(self, request, *args, **kwargs):
        activity = self.get_activity(kwargs['uuid'])

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


class ActivityRequestView(FindActivityMixin, APIView):
    """
    Activity request view for getting activity's requests and creating/deleting
    """
    serializer_class = UserRequestSerializer

    def get(self, request, *args, **kwargs):
        activity = self.get_activity(uuid=kwargs['uuid'], user=request.user)

        requests = activity.requests.filter(is_deleted=False)

        serializer = self.serializer_class(requests, many=True)

        return Response(data=serializer.data)

    def post(self, request, *args, **kwargs):
        activity = self.get_activity(uuid=kwargs['uuid'], user=request.user)

        if activity.user == request.user:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user_request, created = Request.objects.get_or_create(
            user=request.user,
            activity=activity,
            is_deleted=False)

        if not created:
            user_request.is_deleted = True
            user_request.save(update_fields=['is_deleted'])
            return Response()

        user_request.status = activity.default_status
        user_request.save(update_fields=['status'])

        serializer = self.serializer_class(user_request)

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED)


class RequestView(FindActivityMixin, APIView):
    """
    Request view for activity admin

    POST/DELETE only available for activity owner
    """
    serializer_class = UserRequestSerializer

    def get(self, request, *args, **kwargs):
        activity = self.get_activity(uuid=kwargs['uuid'], user=request.user)

        user_request = get_object_or_404(
            Request,
            uuid=kwargs['request_uuid'],
            activity=activity,
            is_deleted=False)

        serializer = self.serializer_class(user_request)

        return Response(data=serializer.data)

    def post(self, request, *args, **kwargs):
        activity = self.get_activity(uuid=kwargs['uuid'], user=request.user)

        can_edit_activity(activity, request.user, raise_exception=True)

        user_request = get_object_or_404(
            Request,
            uuid=kwargs['request_uuid'],
            activity=activity,
            is_deleted=False)

        user_request.status = RequestStatus.APPROVED
        user_request.save(update_fields=['status'])

        serializer = self.serializer_class(user_request)

        return Response(data=serializer.data)

    def delete(self, request, *args, **kwargs):
        activity = self.get_activity(uuid=kwargs['uuid'], user=request.user)
        can_edit_activity(activity, request.user, raise_exception=True)

        user_request = get_object_or_404(
            Request,
            uuid=kwargs['request_uuid'],
            activity=activity,
            is_deleted=False)

        user_request.status = RequestStatus.DENIED
        user_request.save(update_fields=['status'])

        serializer = self.serializer_class(user_request)

        return Response(data=serializer.data)

# User views


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

# Groups views


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


# Communication views


class GroupPostView(GroupMixin, ListAPIView):
    """
    Get or create posts inside a group
    """
    serializer_class = PostSerializer

    def get_queryset(self):
        group = self.get_group(self.kwargs['uuid'], self.request.user)

        posts = group.posts.filter(is_deleted=False)

        return posts

    def post(self, request, *args, **kwargs):
        group = self.get_group(kwargs['uuid'], request.user)

        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save(group=group, user=request.user)

        return Response(
            status=status.HTTP_201_CREATED,
            data=serializer.data)


class ActivityPostView(FindActivityMixin, ListAPIView):
    """
    Get or create posts inside activity
    """
    serializer_class = PostSerializer

    def get_queryset(self):
        activity = self.get_activity(self.kwargs['uuid'], self.request.user)

        posts = activity.posts.filter(is_deleted=False)

        return posts
    
    def post(self, request, *args, **kwargs):
        activity = self.get_activity(self.kwargs['uuid'], self.request.user)

        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save(activity=activity, user=request.user)
        
        return Response(
            status=status.HTTP_201_CREATED,
            data=serializer.data)


class PostView(PostMixin, PutPatchMixin, APIView):
    """
    Post view

    Only allowed if belongs to the same group/activity as the user

    Post will update it only if the author is accessing it
    """
    serializer_class = FullPostSerializer

    def get(self, request, *args, **kwargs):
        post = self.get_post(kwargs['uuid'], request.user)

        serializer = self.serializer_class(post)

        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data)

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, uuid=kwargs['uuid'], is_deleted=False)

        if post.user != request.user:
            return HttpResponseForbidden()

        serializer = self.serializer_class(post, data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data)

    def delete(self, request, *args, **kwargs):
        post = self.get_post_delete(kwargs['uuid'], request.user)

        post.is_deleted = True
        post.save(update_fields=['is_deleted'])

        return Response(status=status.HTTP_200_OK)


class CommentView(PostMixin, APIView):
    """
    Comment view for adding comments to posts and deleting them
    """
    serializer_class = CommentSerializer

    def post(self, request, *args, **kwargs):
        post = self.get_post(kwargs['uuid'], request.user)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(user=request.user, post=post)

        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

    def delete(self, request, *args, **kwargs):
        # call get post to check if user has access to comment
        self.get_post(kwargs['uuid'], request.user)

        if 'comment_uuid' not in kwargs:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        comment = get_object_or_404(Comment, uuid=kwargs['comment_uuid'])

        if comment.user != request.user:
            return HttpResponseForbidden()

        comment.is_deleted = True
        comment.save(update_fields=['is_deleted'])

        return Response(status=status.HTTP_200_OK)


# Utility views


class GetAddresses(APIView):
    def post(self, request, *args, **kwargs):
        pass
