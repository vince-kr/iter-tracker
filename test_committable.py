from committable import Iteration, get_context


class TestContextGetter(object):
    template_fields = ("count", "daterange", "weeks", "learning", "building")
    context = get_context(template_fields)


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
        assert it["count"] == 5

    def test_iterationReturnsDaterangeAsString(self):
        it = self.set_up()
        assert it["daterange"] == "April 1 - 14"
        it = self.set_up(start_date="2023-03-25")
        assert it["daterange"] == "March 25 - April 7"

    def test_iterationKnowsAboutWeeks(self):
        it = self.set_up()
        assert it["weeks"] == [
            ["day_break"] * 7,
            ["day_break"] * 7,
        ]

    def test_iterationReturnsGoalProperties(self):
        it = self.set_up()
        assert it["learning"].description == "My Learning Goal"
        assert it["building"].description == "My Building Goal"
        assert it["learning"].time_target == "04:00"
        assert it["building"].time_target == "04:30"

    def test_iterationGetsInstantiatedWithStudySessions(self):
        it = self.set_up(
            study_sessions=[
                {
                    "session_date": "2023-04-02",  # second day of the iteration
                    "goal_type": "learning",
                    "start": "20:15",
                    "end": "21:40",
                },
                {
                    "session_date": "2023-04-04",  # fourth day of the iteration
                    "goal_type": "building",
                    "start": "20:00",
                    "end": "20:45",
                },
            ]
        )
        assert it["learning"].time_spent == "01:25"
        assert it["building"].time_spent == "00:45"
        assert it["weeks"][0] == [
            "day_break",
            "day_worked",
            "day_break",
            "day_worked",
            "day_break",
            "day_break",
            "day_break",
        ]

    def test_iterationChecksSessionInsideDaterange(self):
        it = self.set_up()
        valid_session_data = {
            "session_date": "2023-04-02"
        }
        invalid_session_data = {
            "session_date": "2023-05-02"
        }
        assert it.session_out_of_daterange(valid_session_data) == False
        assert it.session_out_of_daterange(invalid_session_data) == True


class TestCloseIteration(object):
    # 1. Write Jinja2 template to show fields:
    #   - Learning goal
    #   - Building goal
    #   - Additional work
    #   - Reflection
    # DONE
    # 2. Write route to show this template (GET)
    # DONE
    # 3. Write route to handle form submission (POST)
    # 4. Read in the current iteration
    # 5. Add new key 'review'
    # 6. Add keys 'learning', 'building', 'extra', 'reflect' with data from form
    # 7. Dump the new dict as a JSON in a <iteration_counter>.json file
    # 8. Make the current live.json file empty
    # 9. BONUS: handle the case where the current live.json file is empty
    pass
