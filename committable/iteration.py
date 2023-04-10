from datetime import date
from collections import UserDict
from .persistence import Persistence
from .goal import Goal
from .days import Days


class Iteration(UserDict):
    """Provides all fields required by the UI"""

    def __init__(
        self,
        count: int,
        start_date: str,
        learning: dict,
        building: dict,
        study_sessions: list[dict],
    ) -> None:
        self._days = Days(date.fromisoformat(start_date))
        self._goals = {"learning": Goal(**learning), "building": Goal(**building)}

        self._study_sessions = study_sessions
        for session in self._study_sessions:
            self.record_study_session(**session)

        self.data = {}
        self.data["count"] = count
        self.data["daterange"] = self._days.daterange_as_string()
        self.data["weeks"] = self._days.by_weeks
        self.data["learning"] = self._goals["learning"]
        self.data["building"] = self._goals["building"]

    def record_study_session(
        self, date: str, goal_type: str, start: str, end: str
    ) -> None:
        """Mark the session's date as 'worked' and increase time spent on goal"""
        self._days[date] = "day_worked"
        session_duration = self._get_session_duration(start, end)
        self._goals[goal_type].increase_time_spent(session_duration)

    def _get_session_duration(self, start: str, end: str) -> int:
        """Calculate duration as int of minutes based on start and end time"""
        start_hr, start_min = int(start[:2]), int(start[3:])
        end_hr, end_min = int(end[:2]), int(end[3:])
        return (end_hr - start_hr) * 60 + end_min - start_min

    @property
    def as_dict(self) -> dict:
        """Return a JSON-ifiable dictionary of data needed to rebuild Iteration object"""
        return {
            "count": self.data["count"],
            "start_date": self._days.first_day,
            "learning": self["learning"].construction_data,
            "building": self["building"].construction_data,
            "study_sessions": self._study_sessions,
        }


def get_context(template_fields: tuple) -> None:
    iteration_data = Persistence.read()
    iteration = Iteration(*iteration_data)
    return {field_name: iteration[field_name] for field_name in template_fields}