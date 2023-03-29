import unittest
from datetime import date, timedelta
from agile import Iteration


class TestIteration(unittest.TestCase):
    def setUp(self):
        duration = 14
        first_day = date.fromisoformat("2023-03-04")
        study_sessions = {date.fromisoformat("2023-03-04")+timedelta(days=i): []
                          for i in range(duration)}
        self.iter_data = {
            "duration": duration,
            "first_day": first_day,
            "goals": {
                "time_goal": "No time",
                "learning_goal": "No learning",
                "build_goal": "No build",
            },
            "study_sessions": study_sessions,
            "counter": 3,
            "testing": True,
        }
        # Instantiate an iteration starting Saturday 4 March 2023 for 2 weeks
        self.it = Iteration(self.iter_data)

    def test_iterationObjectCanReturnCounter(self) -> None:
        self.assertEqual(self.it.counter, 3)

    def test_iterationObjectReturnsStartToEndString(self) -> None:
        self.iter_data["first_day"] = date.fromisoformat("2023-02-18")
        it = Iteration(self.iter_data)
        self.assertEqual(it.start_to_end, "February 18 - March 3")
        self.iter_data["first_day"] = date.fromisoformat("2023-03-04")
        it = Iteration(self.iter_data)
        self.assertEqual(it.start_to_end, "March 4 - 17")

    def test_iterationObjectReturnsListOfWeeks(self) -> None:
        self.assertEqual(self.it.weeks[0][0]["day_of_week"], "Saturday")
        self.assertEqual(self.it.weeks[0][0]["day_and_month"], "4 Mar")
        self.assertEqual(self.it.weeks[0][4]["day_of_week"], "Wednesday")
        self.assertEqual(self.it.weeks[0][4]["day_and_month"], "8 Mar")
        self.assertEqual(self.it.weeks[1][0]["day_of_week"], "Saturday")
        self.assertEqual(self.it.weeks[1][0]["day_and_month"], "11 Mar")

    def test_iterationReportsOnTimeSpentPerGoal(self) -> None:
        today = date.fromisoformat("2023-03-04")
        self.it.generate_new_study_session(today, "build", "12:20", "12:50")
        self.it.generate_new_study_session(
            today + timedelta(days=1), "build", "10:15", "10:45"
        )
        self.it.generate_new_study_session(
            today + timedelta(days=4), "learning", "06:40", "07:10"
        )
        self.it.generate_new_study_session(
            today + timedelta(days=10), "learning", "20:30", "21:00"
        )
        self.assertEqual(self.it.time_spent_per_goal, {"learning": 60, "build": 60})

    def test_ifStudySessionsOverlap_raisesAttributeError(self) -> None:
        day = date.fromisoformat("2023-03-04")
        self.it.generate_new_study_session(day, "build", "20:00", "21:00")
        with self.assertRaises(AttributeError):
            self.it.generate_new_study_session(day, "build", "19:30", "20:30")
            self.it.generate_new_study_session(day, "learning", "20:00", "20:30")

    def test_iterationReturnsGoals(self):
        self.iter_data["goals"][
            "time_goal"
        ] = "240 minutes learning / 360 minutes build"
        self.iter_data["goals"]["learning_goal"] = "Some pages"
        self.iter_data["goals"]["build_goal"] = "A cool app"
        it = Iteration(self.iter_data)
        self.assertEqual("240 minutes learning / 360 minutes build", it.time_goal)
        self.assertEqual("Some pages", it.learning_goal)
        self.assertEqual("A cool app", it.build_goal)

    def testIterationReturnsDictForPersistence(self):
        self.it.generate_new_study_session(
            date.fromisoformat("2023-03-04"), "build", "20:30", "21:30"
        )
        self.it.generate_new_study_session(
            date.fromisoformat("2023-03-06"), "learning", "14:00", "14:40"
        )
        self.assertEqual(
            {
                "start": "2023-03-04",
                "duration": 14,
                "goals": {
                    "time_goal": "No time",
                    "learning_goal": "No learning",
                    "build_goal": "No build",
                },
                "study_sessions": {
                    "2023-03-04": [
                        {
                            "goal": "build",
                            "start": "20:30",
                            "end": "21:30",
                        }
                    ],
                    "2023-03-05": [],
                    "2023-03-06": [
                        {
                            "goal": "learning",
                            "start": "14:00",
                            "end": "14:40",
                        }
                    ],
                    "2023-03-07": [],
                    "2023-03-08": [],
                    "2023-03-09": [],
                    "2023-03-10": [],
                    "2023-03-11": [],
                    "2023-03-12": [],
                    "2023-03-13": [],
                    "2023-03-14": [],
                    "2023-03-15": [],
                    "2023-03-16": [],
                    "2023-03-17": [],
                },
            },
            self.it.get_persistence_data(),
        )


class TestAgile(unittest.TestCase):
    pass


if __name__ == "__main__":
    unittest.main()