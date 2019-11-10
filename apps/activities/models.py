from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property

from apps.utils.constants import Currencies
from apps.utils.models import BaseModel, Tag, Address
from apps.users.models import User

from .constants import RequestStatus, ActivityFormat


class ActivityType(BaseModel):
    title = models.CharField(max_length=100)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Activity(BaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    time = models.DateTimeField(default=timezone.now)
    duration = models.IntegerField(
        default=60,
        validators=(
            MinValueValidator(5),
            MaxValueValidator(600)
        )
    )

    address = models.ForeignKey(
        Address,
        related_name='activities',
        null=True,
        on_delete=models.DO_NOTHING)

    group = models.ForeignKey(
        'groups.Group',
        null=True,
        blank=True,
        on_delete=models.CASCADE)

    activity_type = models.ForeignKey(
        to=ActivityType,
        null=True,
        blank=True,
        related_name='activities',
        on_delete=models.SET_NULL)

    tags = models.ManyToManyField(
        to=Tag,
        blank=True,
        related_name='activities')

    user = models.ForeignKey(
        to=User,
        related_name='activities',
        null=False,
        on_delete=models.CASCADE)

    public = models.BooleanField(default=True)
    needs_approval = models.BooleanField(default=True)

    FORMAT = None

    def __str__(self):
        return self.title

    @cached_property
    def child(self):
        """ Get subchild of the activity """
        try:
            activity = GroupActivity.objects.get(uuid=self.uuid)
        except:
            try:
                activity = IndividualActivity.objects.get(uuid=self.uuid)
            except:
                activity = None
        return activity


class IndividualActivity(Activity):
    FORMAT = ActivityFormat.INDIVIDUAL


class GroupActivity(Activity):
    max_attendees = models.IntegerField(
        default=5,
        validators=(
            MinValueValidator(2),
            MaxValueValidator(500)
        ))

    price = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        default=Decimal(0))
        
    currency = models.CharField(
        max_length=30,
        choices=Currencies.CHOICES,
        default=Currencies.DKK)

    FORMAT = ActivityFormat.GROUP


class Request(BaseModel):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    status = models.CharField(
        max_length=12,
        choices=RequestStatus.CHOICES,
        default=RequestStatus.PENDING)
    
    message = models.TextField(null=True, blank=True)