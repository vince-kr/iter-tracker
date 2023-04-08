import pytest
from agile import Iteration
from datetime import date


class TestIteration(object):
    def set_up(self):
        count = 5
        start_date = date.fromisoformat("2023-04-01")
        learning = (
            "My Learning Goal",
            240,  # 04:00
            0,
        )
        building = (
            "My Building Goal",
            270,  # 04:30
            0,
        )
        self.it = Iteration(
            count=count, start_date=start_date, learning=learning, building=building
        )

    def test_iterationReturnsCurrentCount(self):
        self.set_up()
        assert self.it.count == 5

    def test_iterationReturnsGoalProperties(self):
        self.set_up()
        assert self.it.learning.description == "My Learning Goal"
        assert self.it.learning.time_target == "04:00"
        assert self.it.building.time_target == "04:30"
        assert self.it.learning.time_spent == "00:00"
        assert self.it.building.spent_as_percentage == "0.00%"

    def test_iterationKnowsAboutWeeks(self):
        self.set_up()
        assert self.it.weeks == [
            ["day_break"] * 7,
            ["day_break"] * 7,
        ]

    def test_iterationCanRegisterStudySessions(self):
        self.set_up()
        new_sesh = {
            "date": "2023-04-02",  # second day of the iteration
            "goal_type": "learning",
            "start": "20:15",
            "end": "21:40",
        }
        self.it.record_study_session(**new_sesh)
        assert self.it.learning.time_spent == "01:25"
        assert self.it.learning.spent_as_percentage == "35.42%"
        assert self.it.weeks[0] == [
            "day_break",
            "day_worked",
            "day_break",
            "day_break",
            "day_break",
            "day_break",
            "day_break",
        ]
