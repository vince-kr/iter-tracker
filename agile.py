from goal import Goal
from days import Days


class Iteration:
    """Provides all fields required by the UI"""

    def __init__(
        self,
        count: int,
        start_date: object,
        learning: tuple,
        building: tuple,
        study_sessions: list[dict],
    ) -> None:
        self.count = count

        self._days = Days(start_date)
        self.daterange = self._days.daterange_as_string()

        self._goals = {"learning": Goal(*learning), "building": Goal(*building)}
        self.learning = self._goals["learning"]
        self.building = self._goals["building"]

        for session in study_sessions:
            self.record_study_session(**session)

    @property
    def weeks(self) -> list:
        """Return the iteration's days as a list of two lists of 7 days each"""
        return self._days.by_weeks

    def record_study_session(self, date: str, goal_type: str, start: str, end: str) -> None:
        """Mark the session's date as 'worked' and increase time spent on goal"""
        self._days[date] = "day_worked"
        session_duration = self._get_session_duration(start, end)
        self._goals[goal_type].increase_time_spent(session_duration)

    def _get_session_duration(self, start: str, end: str) -> int:
        """Calculate duration as int of minutes based on start and end time"""
        start_hr, start_min = int(start[:2]), int(start[3:])
        end_hr, end_min = int(end[:2]), int(end[3:])
        return (end_hr - start_hr) * 60 + end_min - start_min
