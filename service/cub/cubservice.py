import json
from json import JSONDecodeError
from time import sleep

import requests
from http.cookies import SimpleCookie

from models.cub.calendar import Calendar
from models.cub.pharmacy import Pharmacy

HOST = "https://svu.marketouchmedia.com"
CALENDAR_PATH = "/SVUSched/program/program1987/Calendar/PatientCalendar"
DAY_PATH = "/SVUSched/program/program1987/Calendar/PatientCalendarDay"

COURTESY_TIMEOUT_SECONDS = 0.5


class CubService:

    def __init__(self, cookie: str):
        self.session = requests.Session()
        requests.utils.add_dict_to_cookiejar(self.session.cookies, cookie_dict_from_string(cookie))

    def get_pharmacy_calendar(self, pharmacy: Pharmacy, month: int):
        form_data = {
            "facilityId": pharmacy.facility_id,
            "year": 2021,
            "month": month,
            "snapCalendarToFirstAvailMonth": False
        }

        response = self.session.post(
            HOST + CALENDAR_PATH,
            data=form_data
        )

        sleep(COURTESY_TIMEOUT_SECONDS)

        if response.status_code != 200:
            raise ConnectionError("Request failed", response)

        try:
            response_json = json.loads(response.text)
        except JSONDecodeError as exc:
            print("Cookie expired")
            raise exc

        if not response_json["Success"]:
            raise ConnectionError("Unsuccessful response", response)

        return Calendar(response_json["Data"])

    # def get_calendar_day(self, pharmacy: Pharmacy, month: int, day: int):
    #     form_data = {
    #         "facilityId": pharmacy.facility_id,
    #         "year": 2021,
    #         "month": month,
    #         "snapCalendarToFirstAvailMonth": False
    #     }
    #
    #     response = self.session.post(
    #         HOST + DAY_PATH,
    #         data=form_data
    #     )


def cookie_dict_from_string(cookie_string: str):
    cookie = SimpleCookie()
    cookie.load(cookie_string)
    cookie_dict = {}
    for key, item in cookie.items():
        cookie_dict[key] = item.value
    return cookie_dict


def get(response):
    if response.status_code != 200:
        raise ConnectionError("Request failed", response)