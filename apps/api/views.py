from datetime import datetime
from itertools import chain
import uuid

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponseForbidden, HttpResponseBadRequest

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView

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
    BriefGroupSerializer,
    MembershipSerializer,
    UserMembershipSerializer
)
from apps.groups.utils import has_access, can_edit
from apps.users.models import User
from apps.users.serializers import UserSerializer
from apps.utils.location_utils import get_similar_addresses
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
    group_serializer_class = GroupActivitySerializer

    def get(self, request, *args, **kwargs):
        activity = self.get_activity(kwargs['uuid'], request.user)

        can_view_activity(activity, request.user, raise_exception=True)
        
        if activity.FORMAT == ActivityFormat.INDIVIDUAL:
            serializer = self.individual_serializer_class(activity)
        else:
            serializer = self.group_serializer_class(activity)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        activity = self.get_activity(kwargs['uuid'], request.user)

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
        activity = self.get_activity(kwargs['uuid'], request.user)

        can_edit_activity(activity, request.user, raise_exception=True)

        activity.is_deleted = True
        activity.save(update_fields=['is_deleted'])

        return Response(status=status.HTTP_200_OK)


class ActivityTagsView(FindActivityMixin, APIView):
    """
    View for adding tags to activity
    """
    serializer_class = TagSerializer

    def get(self, request, *args, **kwargs):
        activity = self.get_activity(kwargs['uuid'], request.user)

        tags = activity.tags.all()
        serializer = self.serializer_class(tags, many=True)

        return Response(serializer.data)        

    def post(self, request, *args, **kwargs):
        uuid = kwargs['uuid']
        activity = self.get_activity(kwargs['uuid'], request.user)

        can_edit_activity(activity, request.user, raise_exception=True)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        tag = serializer.save()

        if activity.tags.filter(uuid=tag.uuid).exists():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'detail': 'Tag already added'})

        activity.tags.add(tag)

        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def delete(self, request, *args, **kwargs):
        activity = self.get_activity(kwargs['uuid'], request.user)

        can_edit_activity(activity, request.user, raise_exception=True)

        tag_uuid = request.data.get('uuid', None)

        if tag_uuid:
            try:
                uuid.UUID(tag_uuid)
            except:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={'detail': '{} is not a valid UUID'.format(tag_uuid)})
            
            tag = get_object_or_404(Tag, uuid=tag_uuid)
        else:
            tag_title = request.data.get('title', None)

            if tag_title is None:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={'detail': 'title and uuid undefined'})
            
            tag = get_object_or_404(Tag, title=tag_title)

        activity.tags.remove(tag)

        return Response()


class ActivityTagFilterView(ListAPIView):
    """
    Search activities based on tags
    """
    serializer_class = ActivitySerializer

    def get_queryset(self):
        tag_identifier = self.kwargs.get('identifier', None)
        tag_uuid = None

        try:
            tag_uuid = uuid.UUID(tag_identifier)
        except:
            pass
        
        if tag_uuid:
            tag = get_object_or_404(Tag, uuid=tag_uuid)
        else:
            tag = get_object_or_404(Tag, title=tag_identifier)

        return Activity.objects.filter(
            Q(user=self.request.user) | Q(public=True) |
            Q(
                requests__user=self.request.user,
                requests__status=RequestStatus.APPROVED,
                requests__is_deleted=False
            ),
            is_deleted=False,
            tags=tag
        ).filter(time__gte=datetime.today()).order_by('-time')


class RegisterActivityAddress(FindActivityMixin, APIView):
    """
    Activity address API endpoint
    """
    serializer_class = AddressSerializer

    def get(self, request, *args, **kwargs):
        activity = self.get_activity(kwargs['uuid'], request.user)

        serializer = self.serializer_class(activity.address)

        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def post(self, request, *args, **kwargs):
        activity = self.get_activity(kwargs['uuid'], request.user)

        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        address_instance = serializer.save()

        address_instance.user = request.user
        address_instance.save(update_fields=['user'])

        activity.address = address_instance
        activity.save(update_fields=['address'])

        return Response(status=status.HTTP_201_CREATED, data=serializer.data)


class NearbyActivitiesView(APIView):
    """
    Return the activities nearby coordinates

    Specify `longitude` and `latitude` in the request
    """
    address_serializer_class = MinimalAddressSerializer
    serializer_class = ActivitySerializer

    def get(self, request, *args, **kwargs):
        address_serializer = self.address_serializer_class(data=request.data)

        try:
            address_serializer.is_valid(raise_exception=True)
        except:
            address_serializer = self.address_serializer_class(data=request.GET)
            address_serializer.is_valid(raise_exception=True)

        address_instance = address_serializer.save()

        address_instance.user = request.user
        address_instance.save(update_fields=['user'])

        activities = find_close_to_address(address_instance)

        serializer = self.serializer_class(activities, many=True)

        return Response(status=status.HTTP_200_OK, data=serializer.data)


class SearchActivitiesView(APIView):
    """
    Search activities
    """
    serializer_class =  ActivitySerializer

    def get(self, request, *args, **kwargs):
        query = request.data.get('query', None)
        
        if query is None:
            query = request.GET.get('query', None)

        memberships = request.user.memberships.filter(status=RequestStatus.APPROVED)

        activities = Activity.objects.filter(Q(user=request.user) | Q(public=True), is_deleted=False)
        groups = request.user.owned_groups.filter(is_deleted=False)
        requests = request.user.requests.filter(
            Q(status=RequestStatus.PENDING) | Q(status=RequestStatus.APPROVED), is_deleted=False)

        for group in groups:
            activities |= group.activities.filter(is_deleted=False)
        
        for membership in memberships:
            activities |= membership.group.activities.filter(is_deleted=False)

        for r in requests:
            activities |= Activity.objects.filter(pk=r.activity.pk)

        if query is not None:
            activities = activities.filter(
                Q(title__contains=query) | Q(description__contains=query))

        serializer = self.serializer_class(activities, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class ActivityRequestView(FindActivityMixin, APIView):
    """
    Activity request view for getting activity's requests and creating/deleting
    """
    serializer_class = RequestSerializer

    def get(self, request, *args, **kwargs):
        activity = self.get_activity(uuid=kwargs['uuid'], user=request.user)

        requests = activity.requests.filter(is_deleted=False)

        serializer = self.serializer_class(requests, many=True)

        return Response(data=serializer.data)

    def post(self, request, *args, **kwargs):
        activity = self.get_activity(uuid=kwargs['uuid'], user=request.user)

        # check if the request already exists
        user_request = Request.objects.filter(
            user=request.user, 
            activity=activity, 
            is_deleted=False)

        if hasattr(activity, 'max_attendees'):
            # it is a group activity, check if it has less than the max_attendees
            if activity.number_of_attendees >= activity.max_attendees:
                return Response(
                    status=status.HTTP_403_FORBIDDEN, data={'detail': 'aready full'})
        elif not user_request.exists():
            # it is an individual activity, check if it has at least one attendee
            if activity.number_of_attendees != 0:
                return Response(
                    status=status.HTTP_403_FORBIDDEN, data={'detail': 'already full'})

        if activity.user == request.user:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user_request, created = Request.objects.get_or_create(
            user=request.user,
            activity=activity,
            is_deleted=False)

        if not created:
            user_request.is_deleted = True
            user_request.save(update_fields=['is_deleted'])
            return Response({'deleted': True})

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
        
        if hasattr(activity, 'max_attendees') and activity.max_attendees >= activity.number_of_attendees:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        elif activity.number_of_attendees != 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)

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


class SelfUserView(RetrieveAPIView):
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(instance=request.user, data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)


class UserTagsView(ListAPIView):
    serializer_class = TagSerializer

    def get_queryset(self):
        return self.request.user.tags.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        tag = serializer.instance

        if request.user.tags.filter(uuid=tag.uuid).exists():
            return Response(
                status=status.HTTP_400_BAD_REQUEST, 
                data={'detail': 'Tag already added'})
        
        request.user.tags.add(tag)

        return Response(
            serializer.data, 
            status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        tag_uuid = request.data.get('uuid', None)

        if tag_uuid:
            try:
                uuid.UUID(tag_uuid)
            except:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={'detail': '{} is not a valid UUID'.format(tag_uuid)})
            
            tag = get_object_or_404(Tag, uuid=tag_uuid)
            request.user.tags.remove(tag)
        else:
            tag_title = request.data.get('title', None)

            tag = get_object_or_404(Tag, title=tag_title)
            request.user.tags.remove(tag)

        return Response()


class UserActivitiesView(ListAPIView):
    """ Get future user activities """
    serializer_class = ActivitySerializer

    def get_queryset(self):
        return Activity.objects.filter(
            time__gte=datetime.today(),
            is_deleted=False
        ).filter(
            Q(user=self.request.user) | Q(
                requests__user=self.request.user,
                requests__status=RequestStatus.APPROVED,
                requests__is_deleted=False
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

        return Response(
            status=status.HTTP_201_CREATED, 
            data=serializer.data)

# Groups views


class GroupView(GroupMixin, PutPatchMixin, APIView):
    """
    User group view
    """
    serializer_class = BriefGroupSerializer

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
        user_identifier = request.data.get('user', None)
        # TODO remove this
        # membership_status = RequestStatus.APPROVED if not group.needs_approval else RequestStatus.PENDING

        if user_uuid:
            user = get_object_or_404(User, uuid=user_uuid)
        elif user_identifier:
            user = User.objects.filter(Q(email=user_identifier) | Q(username=user_identifier))

            if not user.exists():
                return Response(status=status.HTTP_404_NOT_FOUND)

            user = user.first()
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST, 
                data={'detail': 'please specify user_uuid'})

        membership, created = Membership.objects.get_or_create(
            user=user,
            group=group,
            status=RequestStatus.APPROVED,
            membership_type=MembershipTypes.PARTICIPANT)

        serializer = self.serializer_class(membership)

        return Response(
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
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
        print(self.kwargs['uuid'])
        activity = self.get_activity(self.kwargs['uuid'], self.request.user)

        posts = activity.posts.filter(is_deleted=False).order_by('-created_at')

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


class GetSimilarAddressesView(APIView):
    serializer_class = AddressSerializer

    def post(self, request, *args, **kwargs):
        if 'address' not in request.data:
            return HttpResponseBadRequest()

        addresses = get_similar_addresses(request.data['address'])

        serializer = AddressSerializer(addresses, many=True)

        return Response(data=serializer.data)
