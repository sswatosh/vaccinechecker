import time
from datetime import date, timedelta
from python_settings import settings
import webbrowser

import settings as local_settings
from models.cub import pharmacy as pharmacy_model
from models.cub.day import Day
from models.cub.pharmacy import Pharmacy
from service.cub.cubservice import CubService, get_pharmacy_url

settings.configure(local_settings)
assert settings.configured


class CubScraper:

    def __init__(self):
        self.service = CubService(settings.CUB_COOKIE)

    def main(self):
        pharmacies = pharmacy_model.get_known_pharmacies()

        while True:
            months_to_search = get_months_to_search()
            for pharmacy in pharmacies:
                self.check_pharmacy(pharmacy, months_to_search)

            time.sleep(settings.CHECK_INTERVAL_SECONDS)

    def check_pharmacy(self, pharmacy: Pharmacy, months_to_search: [int]):
        for month in months_to_search:
            calendar = self.service.get_pharmacy_calendar(pharmacy=pharmacy, month=month)
            available_days = calendar.get_available_days()
            appointments_found = self.check_available_days(pharmacy, month, available_days)
            if appointments_found:
                break

    def check_available_days(self, pharmacy: Pharmacy, month: int, days_to_search: [int]):
        for search_day in days_to_search:
            day = self.service.get_day(pharmacy, month, search_day)
            if day.has_rows():
                alert(pharmacy, day)
                return True
        return False


def alert(pharmacy: Pharmacy, day: Day):
    print("APPOINTMENT GET")
    print(pharmacy.name + "," + str(pharmacy.zipcode) + ": " + day.date)
    for row in day.rows:
        print(row)
    print("")
    webbrowser.open(get_pharmacy_url(pharmacy), new=1)


def get_months_to_search():
    today = date.today()
    search_end = today + timedelta(days=settings.CUB_SEARCH_DAYS)

    return {today.month, search_end.month}


if __name__ == "__main__":
    scraper = CubScraper()
    scraper.main()
