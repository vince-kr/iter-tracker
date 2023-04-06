class Iteration:
    def __init__(self, count: int, learning: dict, building: dict) -> None:
        self.count = count
        self._learning = learning
        self._building = building
        self._study_sessions = []

    @property
    def learning(self) -> dict:
        return {
            "description": self._learning["description"],
            "time_target": self._int_of_minutes_to_time_string(
                self._learning["time_target"]
            ),
            "time_spent": self._get_time_spent("learning"),
            "spent_over_target": self._get_spent_over_target("learning"),
        }

    @property
    def building(self) -> dict:
        return {
            "description": self._building["description"],
            "time_target": self._int_of_minutes_to_time_string(
                self._building["time_target"]
            ),
            "time_spent": self._get_time_spent("building"),
            "spent_over_target": self._get_spent_over_target("building"),
        }

    def _int_of_minutes_to_time_string(self, minutes: int) -> str:
        return f"{minutes//60:02d}:{minutes%60:02d}"

    def _get_time_spent(self, goal_type: str) -> str:
        all_durations = [
            sesh["duration"]
            for sesh in self._study_sessions
            if sesh["goal_type"] == goal_type
        ]
        minutes = sum(all_durations)
        return f"{minutes//60:02d}:{minutes%60:02d}"

    def _get_spent_over_target(self, goal_type: str) -> str:
        all_durations = [
            sesh["duration"]
            for sesh in self._study_sessions
            if sesh["goal_type"] == goal_type
        ]
        if goal_type == "learning":
            target = self._learning["time_target"]
        else:
            target = self._building["time_target"]
        return f"{sum(all_durations)/target*100:.2f}%"

    def record_study_session(
        self, date: str, goal_type: str, start: str, end: str
    ) -> None:
        self._study_sessions.append(
            {
                "date": date,
                "goal_type": goal_type,
                "start": start,
                "end": end,
                "duration": self._get_session_duration(start, end),
            }
        )

    def _get_session_duration(self, start: str, end: str) -> int:
        start_hr, start_min = int(start[:2]), int(start[3:])
        end_hr, end_min = int(end[:2]), int(end[3:])
        return (end_hr - start_hr) * 60 + end_min - start_min
