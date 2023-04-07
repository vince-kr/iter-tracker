from goal import Goal


class Iteration:
    def __init__(self, count: int, learning: tuple, building: tuple) -> None:
        self.count = count
        self.goals = {"learning": Goal(*learning), "building": Goal(*building)}
        self._study_sessions = []

    @property
    def learning(self) -> object:
        return self.goals["learning"]

    @property
    def building(self) -> object:
        return self.goals["building"]

    def record_study_session(
        self, date: str, goal_type: str, start: str, end: str
    ) -> None:
        self.goals[goal_type].minutes_spent = self._get_session_duration(start, end)

    def _get_session_duration(self, start: str, end: str) -> int:
        start_hr, start_min = int(start[:2]), int(start[3:])
        end_hr, end_min = int(end[:2]), int(end[3:])
        return (end_hr - start_hr) * 60 + end_min - start_min
