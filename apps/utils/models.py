from django.db import models

import uuid


class Model(models.Model):
    """ Minimum abstract model with UUID """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True


class BaseModel(Model):
    """ Abstract base model """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Address(Model):
    """
    Address element to store locations
    """
    address = models.CharField(max_length=200, blank=True, null=True)

    street = models.CharField(max_length=100, blank=True, null=True)
    streen_number = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    country_short = models.CharField(max_length=10, blank=True, null=True)
    postal_code = models.CharField(max_length=100, blank=True, null=True)

    latitude = models.DecimalField(max_digits=12, decimal_places=5, null=True, blank=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=5, null=True, blank=True)

    google_place_id = models.CharField(max_length=100, null=True, blank=True)
    global_code = models.CharField(max_length=100, null=True, blank=True)

    address_type = models.CharField(max_length=100, null=True, blank=True)

    user = models.ForeignKey(
        'users.User',
        related_name='addresses',
        on_delete=models.SET_NULL,
        null=True,
        blank=True)

    def __str__(self):
        if self.user:
            return '{0} of {1}'.format(self.address, str(self.user))

        return self.address


class Tag(Model):
    """ Used for hashtagging activities, following 'streams'"""
    title = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.title
    
    class Meta:
        indexes = [
            models.Index(fields=('title',))
        ]
