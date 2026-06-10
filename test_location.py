from services.location import get_coordinates
from services.hospitals import get_nearby_hospitals
from services.routes import get_route, traffic_status

print("Step 1")

lat, lon = get_coordinates("Hyderabad")

print("Step 2")

hospitals = get_nearby_hospitals(lat, lon)

print("Step 3")

hospital = hospitals[0]

print("Selected:", hospital["name"])

distance, eta = get_route(
    lat,
    lon,
    hospital["lat"],
    hospital["lon"]
)
traffic = traffic_status(eta)


print("Step 4")

print("Hospital:", hospital["name"])
print("Distance:", distance, "km")
print("ETA:", eta, "mins")
print("Traffic:", traffic)