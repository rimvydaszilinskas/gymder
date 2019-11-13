from django.http import HttpResponseForbidden

from apps.activities.constants import RequestStatus

from .constants import MembershipTypes


def has_access(user, group, raise_exception=False):
    if group.user == user:
        return True
    
    memberships = group.membershps.filter(
        user=user,
        is_deleted=False,
        status=RequestStatus.APPROVED)

    return memberships.exists()

    if raise_exception:
        raise HttpResponseForbidden()
    
    return False


def can_edit(user, group, raise_exception=False):
    if not group:
        if raise_exception:
            raise HttpResponseForbidden()
        return False

    if group.user == user:
        return True
    
    memberships = group.membershps.filter(
        user=user,
        is_deleted=False,
        status=RequestStatus.APPROVED,
        membership_type=MembershipTypes.ADMIN)

    return memberships.exists()

    if raise_exception:
        raise HttpResponseForbidden()
    
    return False
