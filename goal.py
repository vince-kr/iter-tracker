from collections import UserDict


class Goal:
    def __init__(
        self, description: str, target_in_minutes: int, minutes_spent: int = 0
    ) -> None:
        self.description = description
        self._target_in_minutes = target_in_minutes
        self._minutes_spent = minutes_spent

    @property
    def time_target(self) -> str:
        return self._format_time_string(self._target_in_minutes)

    @property
    def time_spent(self) -> str:
        return self._format_time_string(self._minutes_spent)

    @time_spent.setter
    def time_spent(self, value: int) -> None:
        self._minutes_spent += value

    @property
    def spent_as_percentage(self) -> str:
        as_perc = self._minutes_spent / self._target_in_minutes * 100
        return f"{as_perc:.2f}%"

    def _format_time_string(self, minutes) -> str:
        hrs = minutes // 60
        mins = minutes % 60
        return f"{hrs:02d}:{mins:02d}"
