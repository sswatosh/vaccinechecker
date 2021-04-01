from datetime import date, timedelta
from python_settings import settings

import settings as local_settings
from models.cub import pharmacy as pharmacy_model
from models.cub.pharmacy import Pharmacy
from service.cub.cubservice import CubService

settings.configure(local_settings)
assert settings.configured


class CubScraper:

    def __init__(self):
        self.service = CubService(settings.CUB_COOKIE)

    def main(self):
        pharmacies = pharmacy_model.get_known_pharmacies()
        months_to_search = get_months_to_search()

        for pharmacy in pharmacies:
            self.check_pharmacy(pharmacy, months_to_search)

    def check_pharmacy(self, pharmacy: Pharmacy, months_to_search: [int]):
        print("Checking " + pharmacy.name)
        for month in months_to_search:
            calendar = self.service.get_pharmacy_calendar(pharmacy=pharmacy, month=month)
            available_days = calendar.get_available_days()
            if len(available_days) > 0:
                print("Month " + str(month) + ": available Days: " + str(available_days))
            else:
                print("Month " + str(month) + ": no days available")

    # def check_days_in_month(self, pharmacy: Pharmacy, month: int, days: [int]):


def get_months_to_search():
    today = date.today()
    search_end = today + timedelta(days=settings.CUB_SEARCH_DAYS)

    return {today.month, search_end.month}


if __name__ == "__main__":
    scraper = CubScraper()
    scraper.main()
