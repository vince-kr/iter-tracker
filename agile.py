from datetime import date, time, timedelta


class _StudySession:
    def __init__(self, goal:str, start:str, end:str) -> None:
        """Instantiate a study session with goal, start time, and end time"""
        self.goal = goal
        self.start = time.fromisoformat(self._formatIsoString(start))
        self.end = time.fromisoformat(self._formatIsoString(end))
        self.duration = self._calculateDuration(start, end)

    def _formatIsoString(self, time:str) -> str:
        if len(time) == 4:
            time = "0" + time
        return time + ":00"

    def _calculateDuration(self, starttime:str, endtime:str) -> int:
        """Helper method to convert string start and end times into minutes"""
        start_hr, start_min = self._formatTimeString(starttime)
        end_hr, end_min = self._formatTimeString(endtime)
        return (end_hr - start_hr) * 60 + end_min - start_min

    def _formatTimeString(self, time:str) -> tuple:
        """Helper method to return tuple of ints (hrs,mins) for a string time"""
        if len(time) == 4:  # in case of missing leading 0 for hours between 0 and 10
            time = "0" + time
        return (int(time[:2]), int(time[3:]))


class _Day:
    def __init__(self, date:object) -> None:
        self.date = date
        self.day_of_week = self.date.strftime("%A")
        self.day_and_month = self.date.strftime("%-d %b")

    def __eq__(self, _o:object) -> bool:
        return self.date == _o.date


class Iteration:
    def __init__(self, iteration_data:dict) -> None:
        id = iteration_data
        self.duration = id["duration"]
        self.first_day = id["first_day"]
        self.days = self._getListOfDays()
        self.last_day = self.days[-1].date
        self.weeks = [self.days[i*7:i*7+7] for i in range(int(self.duration/7))]
        self.start_to_end = self._generateStartToEndString()
        self.time_goal = id["time_goal"]
        self.learning_goal = id["learning_goal"]
        self.build_goal = id["build_goal"]
        self.counter = id["counter"]
        self.study_sessions = { day.date:[] for day in self.days }

    def _getListOfDays(self) -> list:
        """Return a list of Day objects for each day of the iteration"""
        list_of_days = []
        for i in range(self.duration):
            daily_date = self.first_day + timedelta(days = i)
            list_of_days.append(_Day(daily_date))
        return list_of_days

    def _generateStartToEndString(self) -> str:
        """Return a string with the first and last date of the iteration"""
        iteration_spans_multiple_months = (
                self.first_day.strftime("%B") != self.last_day.strftime("%B"))
        firstday_string = self.first_day.strftime("%B %-d")
        if iteration_spans_multiple_months:
            lastday_string = self.last_day.strftime("%B %-d")
        else:
            lastday_string = self.last_day.strftime("%-d")
        return firstday_string + " - " + lastday_string

    def generateSession(self, date:object, goal:str, start:str, end:str) -> None:
        """Add a study session to the list of study sessions"""
        ss = _StudySession(goal, start, end)
        if not self._newSessionOverlapsExisting(date, ss):
            self.study_sessions[date].append(ss)
        else:
            raise AttributeError

    def _newSessionOverlapsExisting(self, date:object, new_session:object) -> bool:
        for existing_session in self.study_sessions[date]:
            if existing_session.start < new_session.start < existing_session.end:
                return True
        return False

    def getStudySessionsForDate(self, date:object) -> list:
        """Return all study session objects for a given date"""
        return self.study_sessions[date]

    def getSessionsTotals(self) -> dict:
        """Sum the minutes spent on learning goal and build goal this day"""
        totals = { "build": 0, "learning": 0 }
        for day in self.study_sessions:
            for sesh in self.study_sessions[day]:
                totals[sesh.goal] += sesh.duration
        return totals


class Agile:
    def __init__(self) -> None:
        iteration_data = {
                "duration": 14,
                "first_day": date.fromisoformat("2023-03-04"),
                "time_goal": "No time",
                "learning_goal": "No learning",
                "build_goal": "No build",
                "counter": 3,
                }
        self.all_iterations = [ Iteration(iteration_data) ]
        self.current_iteration = self.all_iterations[0]
