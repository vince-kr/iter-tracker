import unittest
from agile import StudySession

class TestAgile(unittest.TestCase):

    def testStudySessionReturnsGoalAndDuration(self):
        ss = StudySession("build", "8:00", "9:00")
        self.assertEqual(ss.getGoalAndDuration(), {
            "goal":"Build",
            "duration":60
            })
