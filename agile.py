from datetime import date

class StudySession:
    def __init__(self, goal:str, start:str, end:str) -> None:
        """Instantiate a study session with goal, start time, and end time"""
        self.goal = goal
        self.duration = self._calculateDuration(start, end)

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
    def __init__(self, datestring:str) -> None:
        self.date = date.fromisoformat(
                datestring[:4] + "-" + datestring[4:6] + "-" + datestring[6:]
                )
        self.study_sessions = []

    def getDayOfWeek(self) -> str:
        """Return full name of the weekday (e.g. 'Monday')"""
        return self.date.strftime("%A")

    def getDayAndMonth(self) -> str:
        """Return day of the month and short month name (e.g. '4 Mar')"""
        return self.date.strftime("%-d %b")

    def generateSession(self, goal:str, start:str, end:str) -> None:
        """Add a study session to the day's list of study sessions"""
        self.study_sessions.append(StudySession(goal, start, end))

    def getSessionTotals(self) -> dict:
        """Sum the total minutes spent on learning goal and build goal this day"""
        totals = { "build": 0, "learn": 0 }
        for session in self.study_sessions:
            totals[session.goal] += session.duration
        return totals
