from rest_framework import serializers

from apps.utils.serializers import TagSerializer

from .models import User


class UserSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(format='hex', read_only=True)
    username = serializers.CharField(read_only=True)
    first_name = serializers.CharField(max_length=128, required=False)
    last_name = serializers.CharField(max_length=128, required=False)
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = User
        fields = (
            'uuid',
            'username',
            'first_name',
            'last_name',
            'email'
        )

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save(update_fields=['first_name', 'last_name'])

        return instance

    def save(self, *args, **kwargs):
        if self.instance is None:
            raise Exception('No instance')
        
        self.instance = self.update(
            self.instance, 
            self.validated_data)

        return self.instance


class DetailedUserSerializer(UserSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = UserSerializer.Meta.fields + ('tags',)


class MobileUserSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(format='hex', read_only=True)
    token = serializers.CharField(read_only=True, source='auth_token.key')

    class Meta:
        model = User
        fields = (
            'uuid',
            'username',
            'first_name',
            'last_name',
            'email',
            'token'
        )
