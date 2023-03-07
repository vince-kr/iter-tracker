from datetime import date, time, timedelta


class StudySession:
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


class Day:
    def __init__(self, date:object) -> None:
        self.date = date
        self.study_sessions = []

    def __eq__(self, other) -> bool:
        return self.date == other.date

    def getDayOfWeek(self) -> str:
        """Return full name of the weekday (e.g. 'Monday')"""
        return self.date.strftime("%A")

    def getDayAndMonth(self) -> str:
        """Return day of the month and short month name (e.g. '4 Mar')"""
        return self.date.strftime("%-d %b")

    def generateSession(self, goal:str, start:str, end:str) -> None:
        """Add a study session to the day's list of study sessions"""
        ss = StudySession(goal, start, end)
        if not self._newSessionOverlapsExisting(ss):
            self.study_sessions.append(ss)
        else:
            raise AttributeError

    def _newSessionOverlapsExisting(self, new_session):
        for existing_session in self.study_sessions:
            if existing_session.start < new_session.start < existing_session.end:
                return True
        return False

    def getSessionTotals(self) -> dict:
        """Sum the total minutes spent on learning goal and build goal this day"""
        totals = { "build": 0, "learning": 0 }
        for session in self.study_sessions:
            totals[session.goal] += session.duration
        return totals


class Iteration:
    def __init__(self, start_date:str, duration:int, goals:dict) -> None:
        self.duration = duration
        self.first_day = date.fromisoformat(
                start_date[:4] + "-" + start_date[4:6] + "-" + start_date[6:]
                )
        self.days = [Day(self.first_day+timedelta(days=i)) for i in range(duration)]
        self.last_day = self.days[-1].date
        self.time_goal = goals["time_goal"]
        self.learning_goal = goals["learning_goal"]
        self.build_goal = goals["build_goal"]

    def getStartToEndString(self) -> str:
        """Return a string with the first and last date of the iteration"""
        start_month = self.first_day.strftime("%B")
        end_month = self.last_day.strftime("%B")
        iteration_spans_multiple_months = start_month != end_month
        firstday_string = self.first_day.strftime("%B %-d")
        if iteration_spans_multiple_months:
            lastday_string = self.last_day.strftime("%B %-d")
        else:
            lastday_string = self.last_day.strftime("%-d")
        return firstday_string + " - " + lastday_string

    def getDaterangeAsWeeks(self) -> list:
        """Return a listcomp with the list of days split into weeks"""
        return [self.days[i*7:i*7+7] for i in range(int(self.duration/7))]    
