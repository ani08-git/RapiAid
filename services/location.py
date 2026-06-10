from geopy.geocoders import Nominatim

def get_coordinates(address):
    geolocator = Nominatim(user_agent="rapidaid")

    location = geolocator.geocode(address)

    if location:
        return location.latitude, location.longitude

    return None