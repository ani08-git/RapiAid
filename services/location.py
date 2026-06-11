from geopy.geocoders import Nominatim


def get_coordinates(address):
    try:
        geolocator = Nominatim(user_agent="rapidaid_app")

        location = geolocator.geocode(
            address,
            timeout=10
        )

        if location:
            return location.latitude, location.longitude

        return None

    except Exception:
        return None