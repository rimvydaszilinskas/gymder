from rest_framework import serializers

from apps.users.serializers import UserSerializer

from .models import Group, Membership


class GroupSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(format='hex', read_only=True)
    title = serializers.CharField(max_length=100, required=False)
    description = serializers.CharField(max_length=500, required=False)
    public = serializers.BooleanField(required=False)
    needs_approval = serializers.BooleanField(required=False)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Group
        fields = (
            'uuid',
            'title',
            'description',
            'public',
            'needs_approval',
            'user'
        )

    def create(self, validated_data):
        if 'title' not in validated_data:
            raise serializers.ValidationError('Title has to be defined!')

        return Group.objects.create(**validated_data)

    def save(self, **kwargs):
        if self.instance is None:
            user = kwargs.get('user', None)
            if 'user' not in kwargs:
                raise Exception('add user to kwargs')

            self.instance = self.create(self.validated_data)
            self.instance.user = user
            self.instance.save(update_fields=['user'])
        else:
            self.instance = self.update(self.instance, self.validated_data)

        return self.instance


class MembershipSerializer(serializers.ModelSerializer):
    """
    A read-only membership serializers
    """
    uuid = serializers.UUIDField(format='hex', read_only=True)
    status = serializers.CharField(read_only=True)
    user = UserSerializer(read_only=True)
    membership_type = serializers.CharField(read_only=True)

    class Meta:
        model = Membership
        fields = (
            'uuid',
            'status',
            'user',
            'membership_type'
        )


class UserMembershipSerializer(serializers.ModelSerializer):
    """
    A read-only user membership serializers
    """
    uuid = serializers.UUIDField(format='hex', read_only=True)
    status = serializers.CharField(read_only=True)
    group = GroupSerializer(read_only=True)
    membership_type = serializers.CharField(read_only=True)

    class Meta:
        model = Membership
        fields = (
            'uuid',
            'status',
            'group',
            'membership_type'
        )
