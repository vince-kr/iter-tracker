from datetime import date, time, timedelta
import json


class _StudySession:
    def __init__(self, goal: str, start: str, end: str) -> None:
        """Instantiate a study session with goal, start time, and end time"""
        self.goal = goal
        self.start = time.fromisoformat(start + ":00")
        self.end = time.fromisoformat(end + ":00")
        self.duration = self._calculate_duration(start, end)

    def _calculate_duration(self, start_time: str, end_time: str) -> int:
        """Helper method to convert string start and end times into minutes"""
        start_hr, start_min = self._format_time_string(start_time)
        end_hr, end_min = self._format_time_string(end_time)
        return (end_hr - start_hr) * 60 + end_min - start_min

    @staticmethod
    def _format_time_string(hrs_mins: str) -> tuple:
        """Helper method to return tuple of ints (hrs,mins) for a string time"""
        return int(hrs_mins[:2]), int(hrs_mins[3:])


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
        self._duration = it_da["duration"]
        self._first_day = it_da["first_day"]
        self._days = self._get_list_of_days()
        self._last_day = self._days[-1].date
        self._goals = it_da["goals"]
        self.weeks = [self._days[i * 7:i * 7 + 7] for i in range(int(self._duration / 7))]
        self.start_to_end = self._generate_start_end_string()
        self.time_goal = self._goals["time_goal"]
        self.learning_goal = self._goals["learning_goal"]
        self.build_goal = self._goals["build_goal"]
        self.counter = it_da["counter"]
        self.testing = "testing" in it_da and it_da["testing"]
        if "study_sessions" in it_da:
            self.study_sessions = self._generate_study_sessions_from_persistence(
                                    it_da["study_sessions"])
        else:
            self.study_sessions = {day.date: [] for day in self._days}

    @staticmethod
    def _generate_study_sessions_from_persistence(sessions_per_day: dict) -> dict:
        study_sessions = {}
        for day in sessions_per_day:
            study_sessions[date.fromisoformat(day)] = []
            for session in sessions_per_day[day]:
                study_sessions[date.fromisoformat(day)].append(
                    _StudySession(session["goal"], session["start"], session["end"])
                )
        return study_sessions

    def _get_list_of_days(self) -> list:
        """Return a list of Day objects for each day of the iteration"""
        list_of_days = []
        for i in range(self._duration):
            days_date = self._first_day + timedelta(days=i)
            list_of_days.append(_Day(days_date))
        return list_of_days

    def _generate_start_end_string(self) -> str:
        """Return a string with the first and last date of the iteration"""
        iteration_spans_multiple_months = (
                self._first_day.strftime("%B") != self._last_day.strftime("%B"))
        first_day_string = self._first_day.strftime("%B %-d")
        if iteration_spans_multiple_months:
            last_day_string = self._last_day.strftime("%B %-d")
        else:
            last_day_string = self._last_day.strftime("%-d")
        return first_day_string + " - " + last_day_string

    def generate_session(self, days_date: object, goal: str, start: str, end: str) -> None:
        """Add a study session to the list of study sessions"""
        ss = _StudySession(goal, start, end)
        if not self._new_session_overlaps_existing(days_date, ss):
            self.study_sessions[days_date].append(ss)
            if not self.testing:
                with open("./persistence/live.json", "w") as iteration_data:
                    json.dump(self.get_persistence_data(), iteration_data, indent=2)
        else:
            raise AttributeError

    def _new_session_overlaps_existing(self, days_date: object, new_session: object) -> bool:
        for existing_session in self.study_sessions[days_date]:
            if existing_session.start <= new_session.start <= existing_session.end:
                return True
        return False

    def get_study_sessions_for_date(self, days_date: object) -> list:
        """Return all study session objects for a given date"""
        return self.study_sessions[days_date]

    def get_sessions_totals(self) -> dict:
        """Sum the minutes spent on learning goal and build goal this day"""
        totals = {"build": 0, "learning": 0}
        for day in self.study_sessions:
            for sesh in self.study_sessions[day]:
                totals[sesh.goal] += sesh.duration
        return totals

    def get_persistence_data(self) -> dict:
        return {
            "start": self._first_day.strftime("%Y-%m-%d"),
            "duration": self._duration,
            "goals": self._goals,
            "study_sessions": self._get_study_sessions_dict()
        }

    def _get_study_sessions_dict(self) -> dict:
        study_sessions_dict = {}
        for day in self.study_sessions:
            study_sessions_dict[day.strftime("%Y-%m-%d")] = []
            for session in self.study_sessions[day]:
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
