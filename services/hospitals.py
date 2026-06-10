import requests


def get_nearby_hospitals(lat, lon):

    query = f"""
    [out:json][timeout:25];
    (
      node["amenity"="hospital"](around:5000,{lat},{lon});
    );
    out body;
    """

    try:
        response = requests.post(
            "https://overpass-api.de/api/interpreter",
            data=query,
            headers={"User-Agent": "RapidAid"}
        )

        print("Status:", response.status_code)
        print(response.text[:300])

        if response.status_code != 200:
            return []

        try:
            data = response.json()
        except Exception:
            return []

        hospitals = []

        for item in data.get("elements", []):
            hospitals.append({
                "name": item.get("tags", {}).get(
                    "name",
                    "Unknown Hospital"
                ),
                "lat": item["lat"],
                "lon": item["lon"]
            })

        return hospitals

    except Exception as e:
        print("Error:", e)
        return []