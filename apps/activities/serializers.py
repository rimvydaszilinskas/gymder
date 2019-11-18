from rest_framework import serializers

from apps.users.serializers import UserSerializer
from apps.utils.constants import Currencies
from apps.utils.models import Tag
from apps.utils.serializers import (
    AddressSerializer,
    TagSerializer
)

from .models import (
    ActivityType,
    GroupActivity,
    IndividualActivity,
    Request
)


class ActivityTypeSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(format='hex', read_only=True)
    title = serializers.CharField(max_length=100)

    class Meta:
        model = ActivityType
        fields = (
            'uuid',
            'title',
            'approved'
        )


class ActivitySerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(format='hex', read_only=True)
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=500, required=False)
    time = serializers.DateTimeField()
    duration = serializers.IntegerField(min_value=5, max_value=600)
    address = AddressSerializer(required=True, many=False)
    activity_type = ActivityTypeSerializer(many=False, required=True)
    public = serializers.BooleanField(required=False)
    needs_approval = serializers.BooleanField(required=False)
    user = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, required=False)
    is_group = serializers.BooleanField(read_only=True)

    class Meta:
        model = IndividualActivity
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
            'tags',
            'is_group'
        )


class IndividualActivitySerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(format='hex', read_only=True)
    title = serializers.CharField(max_length=100, required=True)
    description = serializers.CharField(max_length=500, required=False, allow_blank=True)
    time = serializers.DateTimeField()
    duration = serializers.IntegerField(min_value=5, max_value=600)
    address = AddressSerializer(required=False, many=False)
    activity_type = ActivityTypeSerializer(many=False, required=False)
    public = serializers.BooleanField(required=False)
    needs_approval = serializers.BooleanField(required=False)
    user = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = IndividualActivity
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

    def create(self, validated_data):
        """
        Create a new instance and attach activity type
        """
        tags = validated_data.pop('tags', None)
        activity_type = validated_data.pop('activity_type', None)
        address = validated_data.pop('address', None)

        instance = IndividualActivity(**validated_data)

        if activity_type is not None:
            activity_type_title = activity_type.get('title')
            
            activity_type_object, created = ActivityType.objects.get_or_create(title=activity_type_title)

            instance.activity_type = activity_type_object

        if tags is not None:
            for tag in tags:
                tag_object, created = Tag.objects.get_or_create(title=tag.get('title'))

                instance.tags.add(tag_object)

        return instance

    def update(self, instance, validated_data):
        """
        Update the activity
        To update address, refer to another view in API app
        """
        tags = validated_data.get('tags', None)
        activity_type = validated_data.get('activity_type', None)

        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.time = validated_data.get('time', instance.time)
        instance.duration = validated_data.get('duration', instance.duration)
        instance.public = validated_data.get('public', instance.public)
        instance.needs_approval = validated_data.get('needs_approval', instance.needs_approval)
        
        if activity_type is not None:
            activity_type_title = activity_type.get('title')
            activity_type_object, created = ActivityType.objects.get_or_create(title=activity_type_title.lower())

            instance.activity_type = activity_type_object
            instance.save(update_fields=['activity_type'])

        if tags is not None and isinstance(tags, list):
            instance.tags.clear()
            for tag in tags:
                tag_title = tag.get('title', None)
                tag_object, created = Tag.objects.get_or_create(title=tag_title)

                instance.tags.add(tag_object)

        return instance

    def save(self, *args, **kwargs):
        if self.instance is None:
            user = kwargs.get('user', None)
            if not user:
                raise ValueError('user has to be in kwargs')
            self.instance = self.create(self.validated_data)
            self.instance.user = user
            self.instance.save()
        else:
            self.instance = self.update(self.instance, self.validated_data)

        return self.instance


class GroupActivitySerializer(IndividualActivitySerializer, serializers.ModelSerializer):
    max_attendees = serializers.IntegerField(min_value=2, max_value=20, required=False)
    price = serializers.DecimalField(max_digits=12, decimal_places=4, coerce_to_string=False, required=False)
    currency = serializers.CharField(max_length=30, required=False)
    activity_type = ActivityTypeSerializer(many=False, required=False)
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = GroupActivity
        fields = ActivitySerializer.Meta.fields + (
            'max_attendees',
            'price',
            'currency'
        )

    def validate_currency(self, value):
        if value not in Currencies.ALL:
            raise serializers.ValidationError('Unknown currency')
        return value

    def create(self, validated_data):
        tags = validated_data.pop('tags', None)
        activity_type = validated_data.pop('activity_type', None)
        address = validated_data.pop('address', None)
        instance = GroupActivity(**validated_data)

        if activity_type is not None:
            activity_type_title = activity_type.get('title')
            
            activity_type_object, created = ActivityType.objects.get_or_create(title=activity_type_title)

            instance.activity_type = activity_type_object

        return instance

    def save(self, **kwargs):
        if self.instance is None:
            user = kwargs.get('user', None)
            if not user:
                raise ValueError('user has to be in kwargs')
            self.instance = self.create(self.validated_data)
            self.instance.user = user
            self.instance.save()
        else:
            self.instance = self.update(self.instance, self.validated_data)

        return self.instance


class UserRequestSerializer(serializers.ModelSerializer):
    """ Used for returning events to user view page"""
    uuid = serializers.UUIDField(format='hex', read_only=True)
    activity = ActivitySerializer(read_only=True)

    class Meta:
        model = Request
        fields = (
            'uuid',
            'status',
            'activity',
        )


class RequestSerializer(serializers.ModelSerializer):
    """ Used for returning attendees to event """
    uuid = serializers.UUIDField(format='hex', read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Request
        fields = (
            'uuid',
            'status',
            'activity',
            'message'
        )
