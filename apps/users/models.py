from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext as  _

from apps.utils.models import BaseModel

from .managers import UserManager


class User(BaseModel, AbstractUser):
    """ Main authentication model """
    username = models.CharField(max_length=30, null=True, blank=True, unique=True)
    email = models.EmailField(_('email address'), unique=True, editable=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
