from decimal import Decimal

from rest_framework import serializers

from .location_utils import create_address_from_address, create_address_from_coordinates
from .models import Address, Tag


class AddressSerializer(serializers.ModelSerializer):
    """
    Full address serializer
    On create will collect the data from Google about the location
    Needs to have either address or latitude and longitude passed
    """
    uuid = serializers.UUIDField(format='hex', read_only=True)
    address = serializers.CharField(max_length=200, required=False)
    latitude = serializers.DecimalField(
        max_digits=12,
        decimal_places=5,
        coerce_to_string=False,
        required=False,
        max_value=Decimal(90),
        min_value=Decimal(-90))
    longitude = serializers.DecimalField(
        max_digits=12,
        decimal_places=5,
        coerce_to_string=False,
        required=False,
        max_value=Decimal(180),
        min_value=Decimal(-180))
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
            'country',
            'latitude',
            'longitude'
            )

    def validate(self, data):
        if data.get('address', None) is not None:
            return data
        elif data.get('latitude', None) is not None and \
            data.get('longitude', None) is not None:
            return data
        raise serializers.ValidationError('address or latitude and longitude has to be defined')

    def create(self, validated_data):
        if validated_data.get('address', None) is not None:
            address = create_address_from_address(validated_data['address'])
        else:
            address = create_address_from_coordinates(validated_data['latitude'], validated_data['longitude'])
        
        address.save()
        return address

    def save(self, **kwargs):
        if self.instance is None:
            user = kwargs.get('user', None)
            self.instance = self.create(self.validated_data)

            if user:
                self.instance.user = user
                self.instance.save(update_fields=['user'])
        # We should never update address, instead just discard
        # and leave it hanging for machine learning
        # else:
            # self.instance = self.update(self.validated_data)

        return self.instance


class MinimalAddressSerializer(serializers.ModelSerializer):
    """
    Minimal address serializer
    This should only be used when storing the location from the phone for example
    We retrieve raw coordinates but do not care about the formatted address
    Attach it to the user to have a track of user
    """
    uuid = serializers.UUIDField(format='hex', read_only=True)
    latitude = serializers.DecimalField(
        max_digits=12,
        decimal_places=5,
        coerce_to_string=False,
        required=False,
        max_value=Decimal(90),
        min_value=Decimal(-90))
    longitude = serializers.DecimalField(
        max_digits=12,
        decimal_places=5,
        coerce_to_string=False,
        required=False,
        max_value=Decimal(180),
        min_value=Decimal(-180))

    class Meta:
        model = Address
        fields = (
            'uuid',
            'latitude',
            'longitude'
        )

    def create(self, validated_data):
        return Address.objects.create(
            latitude=validated_data['latitude'], 
            longitude=validated_data[longitude])


    def save(self, **kwargs):
        if self.instance is None:
            user = kwargs.get('user', None)
            self.instance = self.create(self.validated_data)

            self.instance.user = user
            self.instance.save(update_fields=['user'])
        return self.instance


class TagSerializer(serializers.ModelSerializer):
    """
    Tag serializer
    Do not use this to attach tags to the activity
    """
    uuid = serializers.UUIDField(format='hex', read_only=True)
    title = serializers.CharField(max_length=50)

    class Meta:
        model = Tag
        fields = (
            'uuid',
            'title'
        )
