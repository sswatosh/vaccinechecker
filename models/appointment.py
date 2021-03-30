from dataclasses import dataclass


@dataclass
class Appointment:
    location_id: int
    time: str

    def __init__(self, appointment, location_id):
        self.location_id = location_id
        self.time = appointment["time"]

    def __hash__(self):
        return hash(str(self.location_id) + self.time)
