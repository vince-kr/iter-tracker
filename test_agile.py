import unittest
from agile import StudySession, Day, Iteration

class TestStudySession(unittest.TestCase):

    def testStudySessionReturnsGoalAndDuration(self):
        ss = StudySession("build", "8:06", "9:18")
        self.assertEqual(ss.goal, "build")
        self.assertEqual(ss.duration, 72)


class TestDay(unittest.TestCase):

    def testDayReturnsTwoTypesOfDateString(self):
        day = Day("20230304")
        self.assertEqual(day.getDayOfWeek(), "Saturday")
        self.assertEqual(day.getDayAndMonth(), "4 Mar")

    def testDayReturnsSumOfItsSessions(self):
        day = Day("20230304")
        day.generateSession("build", "12:40", "13:30")
        day.generateSession("build", "14:41", "15:16")
        day.generateSession("learn", "20:12", "20:58")
        day.generateSession("learn", "23:08", "23:47")
        self.assertEqual(day.getSessionTotals(), {
            "build":85,
            "learn":85
            })


class TestIteration(unittest.TestCase):

    def TestIterationIsAwareOfItsOwnLength(self):
        it = Iteration("20230304", 14)
