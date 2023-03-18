from datetime import date, timedelta
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
        self.time_goal = self._goals["time_goal"]
        self.learning_goal = self._goals["learning_goal"]
        self.build_goal = self._goals["build_goal"]
        self._counter = it_da["counter"]
        self.testing = "testing" in it_da and it_da["testing"]
        self._study_sessions = {day["date"]: [] for day in self._days}

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
    def study_sessions(self) -> dict:
        return self._study_sessions

    @study_sessions.setter
    def study_sessions(self, value: tuple) -> None:
        day, goal, start, end = value
        self._study_sessions[day].append({
            "goal": goal,
            "start": start,
            "end": end,
            "duration": self._calculate_session_duration(start, end)
        })

    @staticmethod
    def _calculate_session_duration(start_time: str, end_time: str) -> int:
        """Helper method to convert string start and end times into minutes"""
        start_hr, start_min = int(start_time[:2]), int(start_time[3:])
        end_hr, end_min = int(end_time[:2]), int(end_time[3:])
        return (end_hr - start_hr) * 60 + end_min - start_min

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

    # def generate_session(self, days_date: object, goal: str, start: str, end: str) -> None:
    #     """Add a study session to the list of study sessions"""
        # ss = _StudySession(goal, start, end)
        # if not self._new_session_overlaps_existing(days_date, ss):
        #     self.study_sessions[days_date].append(ss)
        #     if not self.testing:
        #         with open("./persistence/live.json", "w") as iteration_data:
        #             json.dump(self.get_persistence_data(), iteration_data, indent=2)
        # else:
        #     raise AttributeError

    def _new_session_overlaps_existing(self, days_date: object, new_session: object) -> bool:
        for existing_session in self.study_sessions[days_date]:
            if existing_session.start <= new_session.start <= existing_session.end:
                return True
        return False

    def get_study_sessions_for_date(self, days_date: object) -> list:
        """Return all study session objects for a given date"""
        return self.study_sessions[days_date]

    def get_sessions_totals(self) -> dict:
        """Sum the minutes spent on learning goal and build goal this iteration"""
        totals = {"build": 0, "learning": 0}
        for day in self.study_sessions:
            for sesh in self.study_sessions[day]:
                totals[sesh.goal] += sesh.duration
        return totals

    def get_persistence_data(self) -> dict:
        return {
            "start": self._first_day.strftime("%Y-%m-%d"),
            "duration": self._length_in_days,
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
