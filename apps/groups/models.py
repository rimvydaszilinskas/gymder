from django.db import models

from apps.activities.constants import RequestStatus
from apps.utils.models import BaseModel

from .constants import MembershipTypes


class Group(BaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField(
        null=True,
        blank=True)
    public = models.BooleanField(default=True)
    needs_approval = models.BooleanField(default=False)

    user = models.ForeignKey(
        'users.User',
        related_name='owned_groups',
        null=True,
        blank=True,
        on_delete=models.SET_NULL)

    def __str__(self):
        return self.title


class Membership(BaseModel):
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE)
    
    status = models.CharField(
        max_length=12,
        choices=RequestStatus.CHOICES,
        default=RequestStatus.APPROVED)

    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE)

    membership_type = models.CharField(
        max_length=12,
        choices=MembershipTypes.CHOICES,
        default=MembershipTypes.PARTICIPANT)

    def __str__(self):
        return '{group} - {user}'.format(group=str(group), user=str(user))
