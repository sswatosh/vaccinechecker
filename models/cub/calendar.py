from dataclasses import dataclass


@dataclass
class CalendarDay:
    number: int
    day_of_week: str
    available: bool

    def __init__(self, day: dict):
        self.number = day["DayNumber"]
        self.day_of_week = day["DayOfWeek"]
        self.available = day["Available"]


@dataclass
class Calendar:
    year: int
    month: int
    days: [CalendarDay]

    def __init__(self, calendar):
        self.year = calendar["Year"]
        self.month = calendar["Month"]
        self.days = [CalendarDay(day) for day in calendar["Days"]]

    def get_available_days(self):
        return {day.number for day in self.days if day.available}
