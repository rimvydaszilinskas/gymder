import math

from django.conf import settings

from .constants import EARTH_RADIUS, EARTH_RADIUS_METERS
from .models import Address


def build_address(geocoded):
    if isinstance(geocoded, list):
        if len(geocoded) == 0:
            raise Exception('Empty list passed to build address')
    
    address = Address()

    # Get full address
    if 'formatted_address' in geocoded:
        address.address = geocoded['formatted_address']

    # Split up the address into parts
    if 'address_components' in geocoded:
        for component in geocoded['address_components']:
            if 'types' in component:
                types = component['types']
                
                if 'street_number' in types:
                    address.streen_number = component['long_name']
                elif 'route' in types:
                    address.street = component['long_name']
                elif 'locality' in types and 'political' in types:
                    address.city = component['long_name']
                elif 'country' in types and 'political' in types:
                    address.country = component['long_name']
                    address.country_short = component['short_name']
                elif 'postal_code' in types:
                    address.postal_code = component['long_name']

    # Get geolocation coordinates
    if 'geometry' in geocoded:
        if 'location' in geocoded['geometry']:
            address.latitude = geocoded['geometry']['location'].get('lat', None)
            address.longitude = geocoded['geometry']['location'].get('lng', None)
    
    # Collect extra data from Google
    # This data is not currently used but it is better to collect it now, rather than later
    if 'place_id' in geocoded:
        address.google_place_id = geocoded['place_id']

    if 'plus_code' in geocoded:
        if 'global_code' in geocoded['plus_code']:
            address.global_code = geocoded['plus_code']['global_code']

    if 'types' in geocoded:
        address.address_type = ','.join(geocoded['types'])

    return address


def _geocode_address(address):
    try:
        geocoded = settings.GOOGLE_MAPS_API.geocode(address)

        if len(geocoded) == 0:
            return None
        
        return geocoded[0]
    except Exception as e:
        print(e)
        return None


def _reverse_geocode_location(lat, lng):
    try:
        geocoded = settings.GOOGLE_MAPS_API.reverse_geocode((lat, lng))

        if len(geocoded) == 0:
            return None

        return geocoded[0]
    except Exception as e:
        print(e)
        return None


def get_address_coordinates(address):
    geocoded = _geocode_address(address)

    if 'geometry' in geocoded:
        if 'location' in geocoded['geometry']:
            if not hasattr(geocoded['geometry']['location'], 'lat') or \
                not hasattr(geocoded['geometry']['location'], 'lng'):
                return None
            return geocoded['geometry']['location']['lat'], geocoded['geometry']['location']['lng']

    return None


def get_geolocation_address(lat, lng):
    response = _reverse_geocode_location(lat, lng)

    if 'formatted_address' in response:
        return response['formatted_address']

    return None


def create_address_from_address(address):
    geocoded = _geocode_address(address)

    return build_address(geocoded)


def create_address_from_coordinates(lat, lng):
    geocoded = _reverse_geocode_location(lat, lng)

    return build_address(geocoded)


def get_distance(from_address, to_address, **kwargs):
    """
    Get distance between two addresses
    Return value is in meters

    Provide `format='km'` in kwargs to return in kilometers
    """

    if not isinstance(from_address, Address) or not isinstance(to_address, Address):
        raise TypeError('Addresses have to be of Address instace')

    if not from_address.latitude or not from_address.longitude \
        or not to_address.latitude or not to_address.longitude:
        raise Exception('latitude and longitude have to be defined!')

    form = kwargs.get('format', None)

    distance = get_distance_haversine(
        from_address.latitude, from_address.longitude,
        to_address.latitude, to_address.longitude)

    if form == 'km':
        return distance / float(1000)
    return distance


def get_distance_haversine(from_lat, from_lon, to_lat, to_lon):
    """ 
    Returns distance between two points using haversine formula 
    Distance is represented in meters
    """
    from_lat = float(from_lat)
    from_lon = float(from_lon)

    to_lat = float(to_lat)
    to_lon = float(to_lon)

    from_lat_rad = math.radians(from_lat)
    from_lon_rad = math.radians(from_lon)
    
    to_lat_rad = math.radians(to_lat)
    ro_lon_rad = math.radians(to_lon)
    
    var1 = math.radians((to_lat - from_lat))
    var2 = math.radians((to_lon - from_lon))

    a = math.sin(var1 / 2.0) ** 2 +\
         math.cos(from_lat_rad) * math.cos(to_lat_rad) * math.sin(var2 / 2.0) ** 2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return c * EARTH_RADIUS_METERS


def get_degree_of_longitude(latitude):
    """ 
    Get distance between two longitude degrees at given latitude
    :return is given in kilometers
    """

    latitude = float(latitude)
    return float(math.cos(latitude) * 111.6)
