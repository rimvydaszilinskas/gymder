from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext as  _
from django.utils.functional import cached_property

from apps.utils.models import BaseModel, Address, Tag

from .managers import UserManager


class User(BaseModel, AbstractUser):
    """ Main authentication model """
    username = models.CharField(max_length=30, null=True, blank=True, unique=True)
    email = models.EmailField(_('email address'), unique=True, editable=False)
    address = models.ForeignKey(
        Address,
        null=True,
        blank=True,
        related_name='default_user',
        on_delete=models.SET_NULL)

    tags = models.ManyToManyField(
        to=Tag,
        related_name='followers',
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    @cached_property
    def created_activities(self):
        return self.activities.only_active()
