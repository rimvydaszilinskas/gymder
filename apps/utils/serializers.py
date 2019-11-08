from rest_framework import serializers

from .models import Address, Tag


class AddressSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(format='hex', read_only=True)
    address = serializers.CharField(max_length=200)
    street = serializers.CharField(read_only=True)
    street_number = serializers.CharField(read_only=True)
    city = serializers.CharField(read_only=True)
    country = serializers.CharField(read_only=True)

    class Meta:
        model = Address
        fields = (
            'uuid',
            'address',
            'street',
            'street_number',
            'city',
            'country'
            )

    def create(self, validated_data):
        # TODO do some google magic here
        return Address.objects.create(address='Testing')

    def save(self):
        if self.instance is not None:
            self.instance = self.create(self.validated_data)
        else:
            self.instance = self.update(self.validated_data)

        return self.instance


class TagSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(format='hex', read_only=True)
    title = serializers.CharField(max_length=50)

    class Meta:
        model = Tag
        fields = (
            'uuid',
            'title'
        )
