from dataclasses import dataclass


@dataclass
class Pharmacy:
    facility_id: int
    name: str
    zipcode: int


def get_known_pharmacies():
    return [
        Pharmacy(9168, "Minneapolis", 55406),
        Pharmacy(9134, "Brooklyn Park", 55428),
        Pharmacy(9180, "Shakopee", 55378),
        Pharmacy(11150, "St Michael", 55376),
        Pharmacy(9177, "Edina", 55435),
        Pharmacy(11038, "St Louis Park", 55416),
        Pharmacy(9167, "Burnsville", 55337)
    ]
