import requests

API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6Ijg5MzVkOTQ5YjU0MjQ3YmU4NjE4MjFiODY3NmE0MTJmIiwiaCI6Im11cm11cjY0In0="

def get_route(start_lat, start_lon, end_lat, end_lon):

    url = "https://api.openrouteservice.org/v2/directions/driving-car"

    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }

    body = {
        "coordinates": [
            [start_lon, start_lat],
            [end_lon, end_lat]
        ]
    }

    response = requests.post(
        url,
        json=body,
        headers=headers
        )
    print("Route Status:", response.status_code)
    print(response.text[:300])
    response.raise_for_status()

    data = response.json()

    summary = data["routes"][0]["summary"]

    distance = round(summary["distance"] / 1000, 2)
    duration = round(summary["duration"] / 60)

    return distance, duration
def traffic_status(eta):

    if eta < 10:
        return "Normal"

    elif eta < 20:
        return "Moderate"

    else:
        return "Heavy"