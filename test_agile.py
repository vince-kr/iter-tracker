import unittest
from datetime import date, timedelta
from agile import Iteration


class TestIteration(unittest.TestCase):

    def setUp(self):
        # Define mock goals for instantiating Iteration objects
        self.iter_data = {
                "duration": 14,
                "first_day": date.fromisoformat("2023-03-04"),
                "time_goal": "No time",
                "learning_goal": "No learning",
                "build_goal": "No build",
                "counter": 3,
                }
        # Instantiate an iteration starting Saturday 4 March 2023 for 2 weeks
        self.it = Iteration(self.iter_data)

    def testCreateThenRecallStudySession(self):
        self.it.generateSession(
                date.fromisoformat("2023-03-04"), "learning", "20:00", "21:00")
        sesh = self.it.getStudySessionsForDate(date.fromisoformat("2023-03-04"))[0]
        self.assertEqual(sesh.duration, 60)
        self.assertEqual(sesh.goal, "learning")

    def testIterationReturnsWeeksizedSlicesOfDaysList(self):
        self.assertTrue(len(self.it.weeks) == 2)
        self.assertTrue(len(self.it.weeks[0]) == 7)

    def testDayReturnsTwoTypesOfDateString(self):
        self.assertEqual(self.it.weeks[0][0].day_of_week, "Saturday")
        self.assertEqual(self.it.weeks[0][0].day_and_month, "4 Mar")

    def testIterationReturnsTimeSpentOnGoals(self):
        today = date.fromisoformat("2023-03-04")
        self.it.generateSession(today, "build", "12:20", "12:50")
        self.it.generateSession(today+timedelta(days=1), "build", "10:15", "10:45")
        self.it.generateSession(today+timedelta(days=4), "learning", "06:40", "07:10")
        self.it.generateSession(today+timedelta(days=10), "learning", "20:30", "21:00")
        self.assertEqual(self.it.getSessionsTotals(), {
            "build":60,
            "learning":60
            })

    def testWhenAddingOverlappingStudySessions_RaisesAttrError(self):
        self.it.generateSession(date.today(), "build", "21:10", "21:30")
        with self.assertRaises(AttributeError):
            self.it.generateSession(date.today(), "learning", "21:20", "21:50")

    def testIterationReturnsItsOwnDuration(self):
        self.iter_data["first_day"] = date.fromisoformat("2023-02-18")
        it = Iteration(self.iter_data)
        self.assertEqual(it.start_to_end, "February 18 - March 3")
        self.iter_data["first_day"] = date.fromisoformat("2023-03-04")
        it = Iteration(self.iter_data)
        self.assertEqual(it.start_to_end, "March 4 - 17")

    def testIterationReturnsGoals(self):
        self.iter_data["time_goal"] = "240 minutes learning / 360 minutes build"
        self.iter_data["learning_goal"] = "Some pages"
        self.iter_data["build_goal"] = "A cool app"
        it = Iteration(self.iter_data)
        self.assertEqual(it.learning_goal, "Some pages")
        self.assertEqual(it.build_goal, "A cool app")


class TestAgile(unittest.TestCase):
    pass
