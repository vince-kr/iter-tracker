class StudySession:
    def __init__(self, goal:str, start:str, end:str) -> None:
        """Instantiate a study session with goal, start time, and end time"""
        self.goal = goal.capitalize()
        self.duration = self._getDuration(start, end)

    def getGoalAndDuration(self) -> dict:
        """Return a dict with the goal worked on and duration of the session"""
        return {
                "goal":self.goal,
                "duration":self.duration
                }

    def _getDuration(self, starttime:str, endtime:str) -> int:
        """Helper method to convert string start and end times into minutes"""
        start_hr, start_min = self._formatTimeString(starttime)
        end_hr, end_min = self._formatTimeString(endtime)
        return (end_hr - start_hr) * 60 + end_min - start_min

    def _formatTimeString(self, time:str) -> tuple:
        """Helper method to return tuple of ints (hrs,mins) for a string time"""
        if len(time) == 4:  # in case of missing leading 0 for hours between 0 and 10
            time = "0" + time
        return (int(time[:2]), int(time[3:]))
