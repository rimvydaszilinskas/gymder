from django.http import HttpResponseForbidden

from apps.groups.utils import has_access
from apps.utils.location_utils import get_degree_of_longitude, get_distance
from apps.utils.models import Address

from .models import Activity


def can_edit_activity(activity, user, raise_exception=False):
    if activity.user != user:
        raise HttpResponseForbidden()
    return True


def can_view_activity(activity, user, raise_exception=False):
    group = activity.group

    if user.is_superuser() or \
        activity.user == user or \
             activity.public or \
                  has_access(user, activity.group, raise_exception=False):
        return True

    if raise_exception:
        raise HttpResponseForbidden()
    return False


def find_close_to_address(address, distance=10, activity=None):
    """
    Find activities in the distance of address
    """
    if not isinstance(address, Address):
        raise TypeError('address has to be of type apps.utils.Address')
    
    latitude = address.latitude
    longitude = address.longitude

    if not latitude or not longitude:
        raise ValueError('latitude/longitude in address is not defined')

    lat_variation = float(111) / float(distance)
    lon_variation = get_degree_of_longitude(latitude) / float(distance)

    max_lat = float(latitude) + lat_variation
    min_lat = float(latitude) - lat_variation
    max_lon = float(longitude) + lon_variation
    min_lon = float(longitude) - lon_variation

    activities = Activity.objects.filter(
        address__latitude__gte=min_lat,
        address__latitude__lte=max_lat,
        address__longitude__gte=min_lon,
        address__longitude__lte=max_lon,
        is_deleted=False)
    
    if activity:
        activities = activities.exclude([activity])
    
    # TODO remove me if too slow. This is just for validation
    # create an empty queryset to store the filtered results
    filtered_activites = Activity.objects.none()
    
    for activity in activities:
        if not hasattr(activity, address):
            continue
        if not activity.address.latitude or not activity.address.longitude:
            continue

        dist = get_distance(address, activity.address, format='km')

        if dist <= dist:
            filtered_activites.append(activity)
    
    return filtered_activites


def find_close_to_activity(activity, distance=10):
    """
    Find activities close to activity
    """
    if not isinstance(activity, Activity):
        raise TypeError('address has to be of type apps.activities.Activity')

    return find_close_to_address(activity.address, distance=distance, activity=activity)
