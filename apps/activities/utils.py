from django.http import HttpResponseForbidden

from apps.groups.utils import has_access


def can_edit_activity(activity, user, raise_exception=False):
    if activity.user != user:
        raise HttpResponseForbidden()
    return True


def can_view_activity(activity, user, raise_exception=False):
    group = activity.group

    if user.is_superuser() or \
        activity.user == user or \
             activity.public or \
                  has_access(user, activity.group, raise_exception=False):
        return True

    if raise_exception:
        raise HttpResponseForbidden()
    return False
