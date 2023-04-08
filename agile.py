from goal import Goal
from days import Days
from datetime import timedelta


class Iteration:
    def __init__(
        self, count: int, start_date: object, learning: tuple, building: tuple
    ) -> None:
        self.count = count
        self._days = Days(start_date)
        self._goals = {"learning": Goal(*learning), "building": Goal(*building)}

    @property
    def learning(self) -> object:
        return self._goals["learning"]

    @property
    def building(self) -> object:
        return self._goals["building"]

    @property
    def weeks(self) -> list:
        return self._days.by_weeks

    def record_study_session(
        self, date: str, goal_type: str, start: str, end: str
    ) -> None:
        session_duration = self._get_session_duration(start, end)
        self._goals[goal_type].time_spent = session_duration
        self._days[date] = "day_worked"

    def _get_session_duration(self, start: str, end: str) -> int:
        start_hr, start_min = int(start[:2]), int(start[3:])
        end_hr, end_min = int(end[:2]), int(end[3:])
        return (end_hr - start_hr) * 60 + end_min - start_min
