import requests

def get_nearby_hospitals(lat, lon):

    query = f"""
    [out:json][timeout:25];
    (
      node["amenity"="hospital"](around:5000,{lat},{lon});
    );
    out body;
    """

    response = requests.post(
        "https://overpass-api.de/api/interpreter",
        data=query,
        headers={"User-Agent": "RapidAid"}
    )

    print("Status:", response.status_code)

    data = response.json()

    hospitals = []

    for item in data.get("elements", []):
        hospitals.append({
            "name": item.get("tags", {}).get("name", "Unknown Hospital"),
            "lat": item["lat"],
            "lon": item["lon"]
        })

    return hospitals