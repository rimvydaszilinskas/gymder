from django.shortcuts import get_object_or_404

from apps.activities.constants import RequestStatus
from apps.activities.models import Activity
from apps.activities.serializers import ActivitySerializer
from apps.pages.views_mixins import PageViewMixin
from apps.users.serializers import UserSerializer

from .constants import MembershipTypes
from .models import Group, Membership
from .serializer import BriefGroupSerializer, MembershipSerializer, GroupSerializer
from .utils import has_access


class UserGroupsView(PageViewMixin):
    BUNDLE_NAME = 'user_groups'

    def create_js_context(self, request, *args, **kwargs):
        owned_groups = request.user.owned_groups.only_active()

        memberships = request.user.memberships.only_active().filter(status=RequestStatus.APPROVED)

        groups = Group.objects.none()

        for membership in memberships:
            groups |= Group.objects.filter(uuid=membership.group.uuid, is_deleted=False)

        return {
            'owned_groups': BriefGroupSerializer(owned_groups, many=True).data,
            'groups': BriefGroupSerializer(groups, many=True).data
        }


class GroupView(PageViewMixin):
    """
    Group preview page
    """
    BUNDLE_NAME = 'group_view'

    def create_js_context(self, request, *args, **kwargs):
        group = get_object_or_404(Group, uuid=kwargs['uuid'], is_deleted=False)

        has_access(request.user, group, raise_exception=True)

        serialized_group = BriefGroupSerializer(group)
        serialized_user = UserSerializer(request.user)

        self.TITLE = group.title

        return {
            'group': serialized_group.data,
            'user': serialized_user.data
        }


class GroupMembersView(PageViewMixin):
    BUNDLE_NAME = 'group_members'

    def create_js_context(self, request, *args, **kwargs):
        group = get_object_or_404(Group, uuid=kwargs['uuid'], is_deleted=False)

        has_access(request.user, group, raise_exception=True)

        memberships = group.memberships.only_active()

        serialized_group = GroupSerializer(group)
        serialized_memberships = MembershipSerializer(memberships, many=True)
        serialized_user = UserSerializer(request.user)

        self.TITLE = 'Members of {}'.format(group.title)

        return {
            'group': serialized_group.data,
            'memberships': serialized_memberships.data,
            'user': serialized_user.data
        }


class GroupActivitiesView(PageViewMixin):
    BUNDLE_NAME = 'group_activities'

    def create_js_context(self, request, *args, **kwargs):
        group = get_object_or_404(Group, uuid=kwargs['uuid'], is_deleted=False)

        has_access(request.user, group, raise_exception=True)

        activities = Activity.objects.only_active().filter(group=group)

        serialized_activities = ActivitySerializer(activities, many=True)
        serialized_group = GroupSerializer(group)
        serialized_user = UserSerializer(request.user)

        self.TITLE = 'Activities of {}'.format(group.title)

        return {
            'group': serialized_group.data,
            'activities': serialized_activities.data,
            'user': serialized_user.data
        }


class CreateActivityView(PageViewMixin):
    """
    Create activity for the group
    """
    BUNDLE_NAME = 'create_activity'

    def create_js_context(self, request, *args, **kwargs):
        group = get_object_or_404(Group, uuid=kwargs['uuid'], is_deleted=False)

        has_access(request.user, group, raise_exception=True)

        serialized_group = GroupSerializer(group)
        serialized_user = UserSerializer(request.user)

        self.TITLE = 'Create activity for {}'.format(group.title)

        return {
            'group': serialized_group.data,
            'user': serialized_user.data
        }


class CreateGroupView(PageViewMixin):
    """
    Create new group view
    """
    BUNDLE_NAME = 'group_create'

    def create_js_context(self, request, *args, **kwargs):
        serialized_user = UserSerializer(request.user)
        
        return {
            'user': serialized_user.data
        }
