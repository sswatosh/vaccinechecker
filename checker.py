import json
import time
import traceback
import requests
import webbrowser
from typing import Iterable
from geopy.distance import geodesic
from python_settings import settings

import settings as local_settings
from models.location import Location


settings.configure(local_settings)
assert settings.configured


def main():
    print("checking...")
    while True:
        try:
            data = get_mn_data()
            locations = get_locations_with_appointments(data)
            nearby_locations = get_locations_within_threshold(locations)
            locations_with_new_appointments = get_locations_with_new_appointments(nearby_locations)
            alert_for_nearby_locations(locations_with_new_appointments)
        except Exception as exc:
            print(traceback.format_exc())
            print(exc)
        finally:
            time.sleep(settings.CHECK_INTERVAL_SECONDS)


def get_mn_data():
    response = requests.get("https://www.vaccinespotter.org/api/v0/states/" + settings.STATE + ".json")

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
    home_point = (settings.HOME_LATITUDE, settings.HOME_LONGITUDE)

    filtered_locations = []

    for location in locations:
        location_point = (location.latitude, location.longitude)
        distance_miles = geodesic(home_point, location_point).miles

        if distance_miles <= settings.DISTANCE_THRESHOLD_MILES:
            location.distance = distance_miles
            filtered_locations.append(location)

    return filtered_locations


old_appointments = set()


def get_locations_with_new_appointments(locations: [Location]):
    locations_by_id = {location.id: location for location in locations}

    global old_appointments
    current_appointments = set()
    for location in locations:
        current_appointments.update(location.appointments)

    for appointment in old_appointments:
        location = locations_by_id.get(appointment.location_id)
        if location:
            location.appointments.remove(appointment)

    old_appointments = current_appointments

    return filter(lambda location: len(location.appointments) > 0, locations_by_id.values())


def alert_for_nearby_locations(locations: Iterable[Location]):
    for location in locations:
        print("VACCINE GET")
        location.print()
        print("")
        webbrowser.open(location.url, new=1)


if __name__ == "__main__":
    main()
