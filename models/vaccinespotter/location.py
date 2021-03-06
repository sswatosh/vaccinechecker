from dataclasses import dataclass

from models.vaccinespotter.appointment import Appointment


@dataclass
class Location:
    id: int
    url: str
    city: str
    name: str
    provider: str
    provider_brand_name: str
    appointments_available_all_doses: bool
    latitude: float
    longitude: float
    distance: int
    appointments: set

    def __init__(self, feature):
        properties = feature["properties"]
        self.id = properties["id"]
        self.url = properties["url"]
        self.city = properties["city"]
        self.name = properties["name"]
        self.provider = properties["provider"]
        self.provider_brand_name = properties["provider_brand_name"]
        self.appointments_available_all_doses = properties["appointments_available_all_doses"]
        coordinates = feature["geometry"]["coordinates"]
        self.latitude = coordinates[1]
        self.longitude = coordinates[0]
        self.distance = -1
        self.appointments = set(Appointment(appointment, self.id) for appointment in properties["appointments"])

    def print(self):
        print(self.provider_brand_name + ", " + self.city)
        print(("%.1f" % self.distance) + " miles")
        for appointment in self.appointments:
            print("Time: " + appointment.time)
        print(self.url)
