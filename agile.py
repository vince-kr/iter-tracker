from datetime import date, time, timedelta
import json


class _Day:
    def __init__(self, days_date: object) -> None:
        self.date = days_date
        self.day_of_week = self.date.strftime("%A")
        self.day_and_month = self.date.strftime("%-d %b")

    def __eq__(self, _o: object) -> bool:
        return self.date == _o.date


class Iteration:
    def __init__(self, iteration_data: dict) -> None:
        it_da = iteration_data
        self._length_in_days = it_da["duration"]
        self._length_in_weeks = self._length_in_days // 7
        self._first_day = it_da["first_day"]
        self._days = self._get_list_of_days()
        self._last_day = self._days[-1]["date"]
        self._goals = it_da["goals"]
        self._counter = it_da["counter"]
        self._testing = "testing" in it_da and it_da["testing"]
        self._study_sessions = {day["date"]: [] for day in self._days}

# Helper methods to calculate class fields
    def _get_list_of_days(self) -> list:
        """Return a list of Day objects for each day of the iteration"""
        list_of_days = []
        for i in range(self._length_in_days):
            days_date = self._first_day + timedelta(days=i)
            list_of_days.append({
                "date": days_date,
                "day_of_week": days_date.strftime("%A"),
                "day_and_month": days_date.strftime("%-d %b")
            })
        return list_of_days

# Iteration properties required by template - require getters only
    @property
    def counter(self) -> int:
        """Return the position of the iteration in the list of all iterations"""
        return self._counter

    @property
    def start_to_end(self) -> str:
        """Return a string with the first and last date of the iteration"""
        iteration_spans_multiple_months = (
                self._first_day.strftime("%B") != self._last_day.strftime("%B"))
        first_day_string = self._first_day.strftime("%B %-d")
        if iteration_spans_multiple_months:
            last_day_string = self._last_day.strftime("%B %-d")
        else:
            last_day_string = self._last_day.strftime("%-d")
        return first_day_string + " - " + last_day_string

    @property
    def weeks(self) -> list:
        return [self._days[fd:fd+7] for fd in range(0, self._length_in_days, 7)]

    @property
    def time_spent_per_goal(self) -> dict:
        time_spent = {"learning": 0, "build": 0}
        for day in self._study_sessions.values():
            for sesh in day:
                time_spent[sesh["goal"]] += sesh["duration"]
        return time_spent

    @property
    def time_goal(self) -> dict:
        return self._goals["time_goal"]

    @property
    def learning_goal(self) -> dict:
        return self._goals["learning_goal"]

    @property
    def build_goal(self) -> dict:
        return self._goals["build_goal"]

# Logic to handle study sessions
    def get_study_sessions_for_date(self, days_date: object) -> list:
        """Return all study session objects for a given date"""
        return self._study_sessions[days_date]

    def generate_new_study_session(self, day: object, goal: str, start: str, end: str) -> None:
        ss = {
            "goal": goal,
            "start": self._string_to_time_obj(start),
            "end": self._string_to_time_obj(end),
            "duration": self._calculate_session_duration(start, end)
        }
        if self._new_session_overlaps_existing(day, ss["start"], ss["end"]):
            raise AttributeError
        self._study_sessions[day].append(ss)

# noinspection PyMethodMayBeStatic
    def _string_to_time_obj(self, time_string: str) -> object:
        return time.fromisoformat(time_string + ":00")

    def _calculate_session_duration(self, start_time: str, end_time: str) -> int:
        """Helper method to convert string start and end times into minutes"""
        start_hr, start_min = self._time_string_to_ints(start_time)
        end_hr, end_min = self._time_string_to_ints(end_time)
        return (end_hr - start_hr) * 60 + end_min - start_min

# noinspection PyMethodMayBeStatic
    def _time_string_to_ints(self, time_string: str):
        return int(time_string[:2]), int(time_string[3:])

    def _new_session_overlaps_existing(
            self, day: object, new_start: object, new_end: object) -> bool:
        starts_in_existing = any([es["start"] <= new_start < es["end"]
                                  for es in self._study_sessions[day]])
        ends_in_existing = any([es["start"] < new_end <= es["end"]
                                for es in self._study_sessions[day]])
        return starts_in_existing or ends_in_existing

# Persistence logic
    def get_persistence_data(self) -> dict:
        return {
            "start": self._first_day.strftime("%Y-%m-%d"),
            "duration": self._length_in_days,
            "goals": self._goals,
            "study_sessions": self._get_study_sessions_dict()
        }

    def _get_study_sessions_dict(self) -> dict:
        study_sessions_dict = {}
        for day in self._study_sessions:
            study_sessions_dict[day.strftime("%Y-%m-%d")] = []
            for session in self._study_sessions[day]:
                study_sessions_dict[day.strftime("%Y-%m-%d")].append(
                    {
                        "goal": session.goal,
                        "start": session.start.strftime("%H:%M"),
                        "end": session.end.strftime("%H:%M")
                    }
                )
        return study_sessions_dict


class Agile:
    def __init__(self) -> None:
        with open("./persistence/live.json") as iteration_data:
            iteration_data = json.load(iteration_data)
        iteration_data["first_day"] = date.fromisoformat(iteration_data["start"])
        with open("./persistence/count") as c:
            iteration_data["counter"] = c.read()
        self.current_iteration = Iteration(iteration_data)
