import unittest
from datetime import date, timedelta
from agile import StudySession, Day, Iteration

class TestStudySession(unittest.TestCase):

    def testStudySessionReturnsGoalAndDuration(self):
        ss = StudySession("build", "8:06", "9:18")
        self.assertEqual(ss.goal, "build")
        self.assertEqual(ss.duration, 72)


class TestDay(unittest.TestCase):

    def testDayReturnsTwoTypesOfDateString(self):
        day = Day(date.fromisoformat("2023-03-04"))
        self.assertEqual(day.getDayOfWeek(), "Saturday")
        self.assertEqual(day.getDayAndMonth(), "4 Mar")

    def testDayReturnsTotalsPerSession(self):
        day = Day("")  # As long as I don't use the Day's date this can be anything
        day.generateSession("build", "12:40", "13:30")
        day.generateSession("build", "14:41", "15:16")
        day.generateSession("learning", "20:12", "20:58")
        day.generateSession("learning", "23:08", "23:47")
        self.assertEqual(day.getSessionTotals(), {
            "build":85,
            "learning":85
            })
        self.assertEqual(day.getTotalSessionDuration(), 170)

    def testWhenAddingOverlappingStudySessions_DayRaisesAttrError(self):
        day = Day("")
        day.generateSession("build", "21:10", "21:30")
        with self.assertRaises(AttributeError):
            day.generateSession("learning", "21:20", "21:50")


class TestIteration(unittest.TestCase):

    def setUp(self):
        self.mock_goals = {
                "time_goal": "No time",
                "learning_goal": "No learning",
                "build_goal": "No build"
                }

    def testIterationReturnsItsOwnDuration(self):
        it = Iteration("20230218", 14, self.mock_goals)
        self.assertEqual(it.getStartToEndString(), "February 18 - March 3")
        it = Iteration("20230304", 14, self.mock_goals)
        self.assertEqual(it.getStartToEndString(), "March 4 - 17")

    def testIterationReturnsGoalsDict(self):
        goals = {
                "time_goal":"240 minutes learning / 360 minutes build",
                "learning_goal": "Some pages",
                "build_goal": "A cool app"
                }
        it = Iteration("20230304", 14, goals)
        self.assertEqual(it.learning_goal, "Some pages")
        self.assertEqual(it.build_goal, "A cool app")

    def testIterationExposesDayObjectsInsideWeeks(self):
        it = Iteration("20230304", 14, self.mock_goals)
        self.assertEqual(it.days[0], Day(date.fromisoformat("2023-03-04")))
        self.assertEqual(it.days[5], Day(date.fromisoformat("2023-03-09")))

    def testIterationReturnsWeeksIterable(self):
        first_day = date.fromisoformat("2023-03-04")
        it = Iteration("20230304", 14, self.mock_goals)
        self.assertEqual(it.getDaterangeAsWeeks(), [
            [Day(first_day+timedelta(days=i)) for i in range(7)],
            [Day(first_day+timedelta(days=7+i)) for i in range(7)]
            ])
