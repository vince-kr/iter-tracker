class Goal:
    def __init__(
        self, description: str, target_in_minutes: int, minutes_spent: int = 0
    ) -> None:
        self.description = description

        self._target_in_minutes = target_in_minutes
        self.time_target = self._format_time_string(self._target_in_minutes)

        self._minutes_spent = minutes_spent

    def increase_time_spent(self, session_minutes: int) -> None:
        """Increase time spent on goal by the duration of one session"""
        self._minutes_spent += session_minutes

    @property
    def time_spent(self) -> str:
        return self._format_time_string(self._minutes_spent)

    @property
    def spent_as_percentage(self) -> str:
        as_perc = self._minutes_spent / self._target_in_minutes * 100
        return f"{as_perc:.2f}%"

    @staticmethod
    def _format_time_string(minutes) -> str:
        """Return hh:mm string from integer of minutes"""
        hrs = minutes // 60
        mins = minutes % 60
        return f"{hrs:02d}:{mins:02d}"
