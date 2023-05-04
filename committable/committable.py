import os
from datetime import date
from collections import UserDict
from .goal import Goal
from .days import Days

# Set up local persistence
persistence_dir_path = os.path.join(os.path.dirname(__file__), os.pardir, "persistence")
try:
    os.mkdir(persistence_dir_path)
except OSError:
    pass

# Ensure persistence/live.json is referenced
live_iteration_path = os.path.join(persistence_dir_path, "live.json")

# Ensure tests/test_live.json is referenced
test_iteration_path = os.path.join(
    os.path.dirname(__file__), os.pardir, "tests", "test_live.json"
)

# Ensure the count path is referenced
count_path = os.path.join(persistence_dir_path, "count")


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
        super().__init__()
        self._days = Days(date.fromisoformat(start_date))
        self._goals = {"learning": Goal(**learning), "building": Goal(**building)}

        self._study_sessions = study_sessions
        for session in self._study_sessions:
            self._record_study_session(**session)

        self.data = {
            "count": count,
            "daterange": self._days.daterange_as_string,
            "weeks": self._days.by_weeks,
            "learning": self._goals["learning"],
            "building": self._goals["building"],
            "today": date.today().strftime("%Y-%m-%d"),
        }

    def _record_study_session(
            self, session_date: str, goal_type: str, start: str, end: str
    ) -> None:
        """Mark the session's date as 'worked' and increase time spent on goal"""
        self._days[session_date] = "day_worked"
        session_duration = self._get_session_duration(start, end)
        self._goals[goal_type].increase_time_spent(session_duration)

    @staticmethod
    def _get_session_duration(start: str, end: str) -> int:
        """Calculate duration as int of minutes based on start and end time"""
        start_hr, start_min = int(start[:2]), int(start[3:])
        end_hr, end_min = int(end[:2]), int(end[3:])
        return (end_hr - start_hr) * 60 + end_min - start_min

    def session_out_of_daterange(self, session_data: dict) -> bool:
        return session_data["session_date"] not in self._days
