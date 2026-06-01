
import requests

def get_road_distance(lat1, lon1, lat2, lon2):
    """
    Uses OSRM public API — actual road distance
    same engine Delhivery uses internally
    """
    try:
        url = (
            f"http://router.project-osrm.org/route/v1/driving/"
            f"{lon1},{lat1};{lon2},{lat2}"
            f"?overview=false"
        )
        r    = requests.get(url, timeout=10)
        data = r.json()

        if data['code'] == 'Ok':
            route        = data['routes'][0]
            distance_km  = route['distance'] / 1000      # meters → km
            duration_min = route['duration'] / 60        # seconds → mins

            return distance_km, duration_min

    except Exception as e:
        print(f"OSRM error: {e}")

    return None, None

# ── Test ─────────────────────────────────────────────────────
# dist, dur = get_road_distance(2.54978, 150.26512, 12.9846,80.1747)
# print(f"Road distance : {dist:.1f} km")
# print(f"OSRM duration : {dur:.1f} mins")
