import collections
from dataclasses import dataclass
from datetime import date, time, timedelta


class Agile:
    def __init__(self) -> None:
        iteration_data = {
            "first_day": date.fromisoformat("2023-04-01"),
            "duration": 14,
            "goals": {
                "learning": Goal(
                    "Learning goal",
                    "3hrs studying Fluent Python (at least finish ch.5, which is 30 more pages); 1hr practicing TCR.",
                    0,
                    240
                ),
                "build": Goal(
                    "Build goal",
                    "I want to implement showing the progress on an iteration in terms of percentage of the time goal versus how much of the iteration has passed. I also want to keep working on the note transposing problem. Say 3hrs for Iteration-Tracker and 1hr on music.",
                    0,
                    240
                ),
            },
            "study_sessions": StudySessions(),
            "counter": 5,
        }
        self.current_iteration = Iteration(iteration_data)


class Iteration:
    def __init__(self, iteration_data: dict) -> None:
        it_da = iteration_data
        self._length_in_days = it_da["duration"]
        self._first_day = it_da["first_day"]
        self._days = self._get_list_of_days()
        self._last_day = self._days[-1]["date"]
        self._goals = it_da["goals"]
        self._counter = it_da["counter"]
        self._study_sessions = it_da["study_sessions"]

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
        return [self._days[fd: fd + 7] for fd in range(0, self._length_in_days, 7)]

    @property
    def study_sessions(self) -> object:
        """Return the dict of study sessions"""
        return self._study_sessions

    @property
    def goals(self) -> list:
        return self._goals

    # Interface to StudySessions logic
    def generate_new_study_session(self, *args) -> None:
        """Pass arguments on to the appropriate StudySessions method,
        then run persistence"""
        self._study_sessions.generate_new(*args)

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


class StudySessions(collections.UserList):
    def generate_new(self, day: object, goal: str, start: str, end: str) -> None:
        """Add a new study session"""
        new_session = {
            "goal": goal,
            "date": day,
            "start": self._string_to_time_obj(start),
            "end": self._string_to_time_obj(end),
            "duration": self._calculate_session_duration(start, end),
        }
        if self._new_session_overlaps_existing(
                day, new_session["start"], new_session["end"]
        ):
            raise AttributeError
        self.append(new_session)

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
        print(self)
        sessions_on_same_day = [sesh for sesh in self if sesh["date"] == day]
        starts_in_existing = any(
            [es["start"] <= new_start < es["end"] for es in sessions_on_same_day]
        )
        ends_in_existing = any(
            [es["start"] < new_end <= es["end"] for es in sessions_on_same_day]
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


@dataclass
class Goal:
    title: str
    description: str
    _time_spent: int
    _time_target: int

    @property
    def time_spent(self) -> str:
        return self._time_as_string(self._time_spent)

    @property
    def time_target(self) -> str:
        return self._time_as_string(self._time_target)

    @property
    def achieved(self) -> str:
        perc = self._time_spent / self._time_target * 100
        return f"{perc:.2f}"

    def _time_as_string(self, time_in_mins: int) -> str:
        hrs = time_in_mins // 60
        mins = time_in_mins % 60
        return f"{hrs:02d}" + ":" + f"{mins:02d}"
