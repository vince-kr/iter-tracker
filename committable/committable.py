from datetime import date
from collections import UserDict
from . import current_iteration_path, test_iteration_path
from .persistence import Persistence
from .goal import Goal
from .days import Days


class Iteration(UserDict):
    """Provides all fields required by the UI"""

    def __init__(self, count: int, start_date: str, learning: dict, building: dict, study_sessions: list[dict]) -> None:
        super().__init__()
        self._days = Days(date.fromisoformat(start_date))
        self._goals = {"learning": Goal(**learning), "building": Goal(**building)}

        self._study_sessions = study_sessions
        for session in self._study_sessions:
            self.record_study_session(**session)

        self.data = {
            "count": count,
            "daterange": self._days.daterange_as_string,
            "weeks": self._days.by_weeks,
            "learning": self._goals["learning"],
            "building": self._goals["building"],
        }

    def record_study_session(
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


def get_context(template_fields: tuple, testing=False) -> dict:
    if testing:
        persistence_path = test_iteration_path
    else:
        persistence_path = current_iteration_path
    iteration_data = Persistence.read(persistence_path)
    iteration = Iteration(**iteration_data)
    return {field_name: iteration[field_name] for field_name in template_fields}


def record_study_session(session_data: dict) -> str:
    current_iteration = Persistence.read(current_iteration_path)
    current_iteration["study_sessions"].append(session_data)
    error = Persistence.write(current_iteration_path, current_iteration)
    return error
