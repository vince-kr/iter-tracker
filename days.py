from collections import UserDict
from datetime import timedelta


class Days(UserDict):
    def __init__(self, start_date: object) -> None:
        self._first_day = start_date
        self._last_day = self._first_day + timedelta(days=13)
        self.data = {
            (start_date + timedelta(days=i)).strftime("%Y-%m-%d"): "day_break"
            for i in range(14)
        }

    @property
    def by_weeks(self) -> list:
        sorted_tuples = sorted([(key, val) for key, val in self.data.items()])
        values = [val[1] for val in sorted_tuples]
        return [values[:7], values[7:]]

    def daterange_as_string(self):
        daterange_spans_months = self._first_day.strftime(
            "%B"
        ) != self._last_day.strftime("%B")
        start = self._first_day.strftime("%B %-d")
        if daterange_spans_months:
            end = self._last_day.strftime("%B %-d")
        else:
            end = self._last_day.strftime("%-d")
        return f"{start} - {end}"
