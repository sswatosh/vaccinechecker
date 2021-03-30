import json
import time

import requests
from geopy.distance import geodesic

from models.location import Location

HOME_LAT = 0  # update
HOME_LONG = 0  # update
STATE = "AL"  # update
THRESHOLD_MILES = 50
CHECK_INTERVAL_SECONDS = 60


def main():
    while(True):
        print("checking...")
        try:
            data = get_mn_data()
            locations = get_locations_with_appointments(data)
            nearby_locations = get_locations_within_threshold(locations)
            alert_for_nearby_locations(nearby_locations)
        finally:
            time.sleep(CHECK_INTERVAL_SECONDS)


def get_mn_data():
    response = requests.get("https://www.vaccinespotter.org/api/v0/states/" + STATE + ".json")

    if response.status_code != 200:
        raise ConnectionError("Request failed", response)

    return json.loads(response.text)


def get_locations_with_appointments(data: dict):
    if data["type"] != "FeatureCollection":
        raise AttributeError("Unknown data format")
    features = data["features"]

    locations = []
    for feature in features:
        if feature["type"] != "Feature":
            print("Unknown feature type: " + feature["type"])
        properties = feature["properties"]
        if properties["appointments_available_all_doses"] is True:
            if feature["geometry"]["type"] != "Point":
                print("Unknown geometry type: " + feature["geometry"]["type"])
            locations.append(Location(feature))

    return locations


def get_locations_within_threshold(locations: [Location]):
    home_point = (HOME_LAT, HOME_LONG)

    filtered_locations = []

    for location in locations:
        location_point = (location.latitude, location.longitude)
        distance_miles = geodesic(home_point, location_point).miles

        if distance_miles <= THRESHOLD_MILES:
            location.distance = distance_miles
            filtered_locations.append(location)

    return filtered_locations


def alert_for_nearby_locations(locations: [Location]):
    if len(locations) != 0:
        for location in locations:
            print("VACCINE GET")
            location.print()
            print("")


if __name__ == "__main__":
    main()
