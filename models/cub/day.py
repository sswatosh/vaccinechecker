from dataclasses import dataclass


@dataclass
class Day:
    date: str
    is_event: bool
    rows: list

    def __init__(self, day):
        self.date = day["Date"]
        self.is_event = day["IsEvent"]
        self.rows = day["Rows"]

    def has_rows(self):
        return len(self.rows) > 0
