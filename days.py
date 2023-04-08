from collections import UserDict
from datetime import timedelta


class Days(UserDict):
    def __init__(self, start_date: object) -> None:
        self.data = {
            (start_date + timedelta(days=i)).strftime("%Y-%m-%d"): "day_break"
            for i in range(14)
        }

    @property
    def by_weeks(self) -> list:
        sorted_tuples = sorted([(key, val) for key, val in self.data.items()])
        values = [val[1] for val in sorted_tuples]
        return [values[:7], values[7:]]
