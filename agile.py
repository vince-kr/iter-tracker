import collections
from datetime import date, time, timedelta
import json


class Agile:
    def __init__(self) -> None:
        with open("./persistence/live.json") as iteration_data:
            iteration_data = json.load(iteration_data)
        new_iteration_data = {
            "first_day": date.fromisoformat(iteration_data["start"]),
            "duration": iteration_data["duration"],
            "goals": iteration_data["goals"],
        }
        with open("./persistence/count") as c:
            new_iteration_data["counter"] = c.read()
        self.current_iteration = Iteration(new_iteration_data)
        if "study_sessions" in iteration_data:
            self.current_iteration.load_study_sessions_from_persistence(
                iteration_data["study_sessions"]
            )


class Iteration:
    def __init__(self, iteration_data: dict) -> None:
        it_da = iteration_data
        self._length_in_days = it_da["duration"]
        self._first_day = it_da["first_day"]
        self._days = self._get_list_of_days()
        self._last_day = self._days[-1]["date"]
        self._goals = it_da["goals"]
        self._counter = it_da["counter"]
        self._testing = "testing" in it_da and it_da["testing"]
        self._study_sessions = StudySessions({day["date"]: [] for day in self._days})

    def _get_list_of_days(self) -> list:
        """Return a list of Day objects for each day of the iteration"""
        list_of_days = []
        for i in range(self._length_in_days):
            days_date = self._first_day + timedelta(days=i)
            list_of_days.append(
                {
                    "date": days_date,
                    "day_of_week": days_date.strftime("%A"),
                    "day_and_month": days_date.strftime("%-d %b"),
                }
            )
        return list_of_days

    # Iteration properties required by template - require getters only
    @property
    def counter(self) -> int:
        """Return the position of the iteration in the list of all iterations"""
        return self._counter

    @property
    def start_to_end(self) -> str:
        """Return a string with the first and last date of the iteration"""
        iteration_spans_multiple_months = self._first_day.strftime(
            "%B"
        ) != self._last_day.strftime("%B")
        first_day_string = self._first_day.strftime("%B %-d")
        if iteration_spans_multiple_months:
            last_day_string = self._last_day.strftime("%B %-d")
        else:
            last_day_string = self._last_day.strftime("%-d")
        return first_day_string + " - " + last_day_string

    @property
    def weeks(self) -> list:
        """Return a list of weeks with each week a list of 7 days"""
        return [self._days[fd : fd + 7] for fd in range(0, self._length_in_days, 7)]

    @property
    def study_sessions(self) -> object:
        """Return the dict of study sessions"""
        return self._study_sessions

    @property
    def time_spent_per_goal(self) -> dict:
        """Return time spent for both learning and build goals"""
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

    # Interface to StudySessions logic
    def generate_new_study_session(self, *args) -> None:
        """Pass arguments on to the appropriate StudySessions method,
        then run persistence"""
        self._study_sessions.generate_new(*args)
        if not self._testing:
            with open("./persistence/live.json", "w") as iteration_data:
                json.dump(self.get_persistence_data(), iteration_data, indent=2)

    def load_study_sessions_from_persistence(self, study_sessions: dict) -> None:
        """Create a new study sessions dict using data from persistence"""
        for day in study_sessions:
            for sesh in study_sessions[day]:
                session_data = (
                    date.fromisoformat(day),
                    sesh["goal"],
                    sesh["start"],
                    sesh["end"],
                )
                self._study_sessions.generate_new(*session_data)

    # Persistence logic
    def get_persistence_data(self) -> dict:
        """Prepare a dict for JSON-ification"""
        return {
            "start": self._first_day.strftime("%Y-%m-%d"),
            "duration": self._length_in_days,
            "goals": self._goals,
            "study_sessions": self._study_sessions.get_as_dict(),
        }


class StudySessions(collections.UserDict):
    def generate_new(self, day: object, goal: str, start: str, end: str) -> None:
        """Add a new study session - this should become __setitem__ at some point"""
        new_session = {
            "goal": goal,
            "start": self._string_to_time_obj(start),
            "end": self._string_to_time_obj(end),
            "duration": self._calculate_session_duration(start, end),
        }
        if self._new_session_overlaps_existing(
            day, new_session["start"], new_session["end"]
        ):
            raise AttributeError
        self[day].append(new_session)

    # noinspection PyMethodMayBeStatic
    def _string_to_time_obj(self, time_string: str) -> object:
        """Helper method to turn hh:mm string into time object"""
        return time.fromisoformat(time_string + ":00")

    def _calculate_session_duration(self, start_time: str, end_time: str) -> int:
        """Helper method to convert string start and end times into minutes"""
        start_hr, start_min = self._time_string_to_ints(start_time)
        end_hr, end_min = self._time_string_to_ints(end_time)
        return (end_hr - start_hr) * 60 + end_min - start_min

    # noinspection PyMethodMayBeStatic
    def _time_string_to_ints(self, time_string: str):
        """Helper method to returns hr:mn from time string"""
        return int(time_string[:2]), int(time_string[3:])

    def _new_session_overlaps_existing(
        self, day: object, new_start: object, new_end: object
    ) -> bool:
        """Return True if a new session overlaps an existing one on the same day"""
        starts_in_existing = any(
            [es["start"] <= new_start < es["end"] for es in self.data[day]]
        )
        ends_in_existing = any(
            [es["start"] < new_end <= es["end"] for es in self.data[day]]
        )
        return starts_in_existing or ends_in_existing

    def get_as_dict(self) -> dict:
        """Prepare StudySessions dict for JSON-ification:
        Use strings for keys instead of date objects
        Use strings for start & end time instead of time objects"""
        study_sessions_dict = {}
        for day in self:
            study_sessions_dict[day.strftime("%Y-%m-%d")] = []
            for session in self[day]:
                study_sessions_dict[day.strftime("%Y-%m-%d")].append(
                    {
                        "goal": session["goal"],
                        "start": session["start"].strftime("%H:%M"),
                        "end": session["end"].strftime("%H:%M"),
                    }
                )
        return study_sessions_dict
