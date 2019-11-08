from rest_framework import serializers

import uuid

from apps.users.models import User
from apps.users.serializers import UserSerializer
from apps.utils.serializers import AddressSerializer, TagSerializer

from .models import (
    ActivityType,
    Activity,
    GroupActivity,
    IndividualActivity)


class ActivityTypeSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(format='hex', read_only=True)
    title = serializers.CharField(max_length=100)

    class Meta:
        model = ActivityType
        fields = (
            'uuid',
            'title'
        )


class ActivitySerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(format='hex', read_only=True)
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=500)
    time = serializers.DateTimeField()
    duration = serializers.IntegerField(min_value=5, max_value=600)
    address = AddressSerializer(required=True, many=False)
    activity_type = ActivityTypeSerializer(many=False, required=True)
    public = serializers.BooleanField(required=False)
    needs_approval = serializers.BooleanField(required=False)
    user = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Activity
        fields = (
            'uuid',
            'title',
            'description',
            'time',
            'duration',
            'address',
            'activity_type',
            'public',
            'needs_approval',
            'user',
            'tags'
        )

    def save(self, *args, **kwargs):
        if self.instance is None:
            if 'user' not in kwargs:
                raise ValueError('user has to be in kwargs')
            elif not isinstance(kwargs['user'], User):
                raise TypeError('user is not of type User')
            self.instance = self.create(self.validated_data)

            self.instance.user = kwargs['user']
            self.instance.save()
        else:
            self.instance = self.update(self.validated_data)

        return self.instance
