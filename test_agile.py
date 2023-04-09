import pytest
from agile import Iteration, iteration_factory
from datetime import date


class TestIterationFactory(object):
    assert isinstance(iteration_factory(), Iteration)


class TestIteration(object):
    def set_up(
        self,
        count=5,
        start_date="2023-04-01",
        learning={
            "description": "My Learning Goal",
            "target_in_minutes": 240,  # 04:00
        },
        building={
            "description": "My Building Goal",
            "target_in_minutes": 270,  # 04:30
        },
        study_sessions=[],
    ):
        return Iteration(
            count=count,
            start_date=start_date,
            learning=learning,
            building=building,
            study_sessions=study_sessions,
        )

    def test_iterationReturnsCurrentCount(self):
        it = self.set_up()
        assert it.count == 5

    def test_iterationReturnsDaterangeAsString(self):
        it = self.set_up()
        assert it.daterange == "April 1 - 14"
        it = self.set_up(start_date="2023-03-25")
        assert it.daterange == "March 25 - April 7"

    def test_iterationReturnsGoalProperties(self):
        it = self.set_up()
        assert it.learning.description == "My Learning Goal"
        assert it.learning.time_target == "04:00"
        assert it.building.time_target == "04:30"
        assert it.learning.time_spent == "00:00"
        assert it.building.spent_as_percentage == "0.00%"

    def test_iterationKnowsAboutWeeks(self):
        it = self.set_up()
        assert it.weeks == [
            ["day_break"] * 7,
            ["day_break"] * 7,
        ]

    def test_iterationCanRegisterStudySessions(self):
        it = self.set_up()
        new_sesh = {
            "date": "2023-04-02",  # second day of the iteration
            "goal_type": "learning",
            "start": "20:15",
            "end": "21:40",
        }
        it.record_study_session(**new_sesh)
        assert it.learning.time_spent == "01:25"
        assert it.learning.spent_as_percentage == "35.42%"
        assert it.weeks[0] == [
            "day_break",
            "day_worked",
            "day_break",
            "day_break",
            "day_break",
            "day_break",
            "day_break",
        ]

    def test_iterationGetsInstantiatedWithStudySessions(self):
        it = self.set_up(
            study_sessions=[
                {
                    "date": "2023-04-02",  # second day of the iteration
                    "goal_type": "learning",
                    "start": "20:15",
                    "end": "21:40",
                }
            ]
        )
        assert it.learning.time_spent == "01:25"
        assert it.weeks[0] == [
            "day_break",
            "day_worked",
            "day_break",
            "day_break",
            "day_break",
            "day_break",
            "day_break",
        ]

    def test_iterationReturnsJSONifiableDictOfItself(self):
        it = self.set_up()
        assert it.as_dict == {
            "count": 5,
            "start_date": "2023-04-01",
            "learning": {
                "description": "My Learning Goal",
                "target_in_minutes": 240,
            },
            "building": {
                "description": "My Building Goal",
                "target_in_minutes": 270,
            },
            "study_sessions": [],
        }
