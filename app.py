from flask import Flask, render_template, request, redirect, url_for
from agile import Iteration
from datetime import date

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    # iteration = Iteration()
    if request.method == "GET":
        context = {
            "learning": {
                "description": "3hrs studying Fluent Python (at least finish ch.5, which is 30 more pages); 1hr practicing TCR.",
                "time_spent": "0:00",
                "time_target": "4:00",
                "percentage_of_target": "0.00%",
            },
            "building": {
                "description": "I want to implement showing the progress on an iteration in terms of percentage of the time goal versus how much of the iteration has passed. I also want to keep working on the note transposing problem. Say 3hrs for Iteration-Tracker and 1hr on music.",
                "time_spent": "2:15",
                "time_target": "4:00",
                "percentage_of_target": "56.25%",
            },
            "weeks": [
                list(range(7)),
                list(range(7)),
            ],
        }
        return render_template("tracker_page", **context)
    else:  # it's POST
        date_of_session = date.fromisoformat(request.form["session_date"])
        session_data = (
            date_of_session,
            request.form["goal_type"],
            request.form["start_time"],
            request.form["end_time"],
        )
        add_study_session_to_current_iteration(iteration, session_data)
        return redirect(url_for("index"))


def add_study_session_to_current_iteration(
        iteration: object, session_data: tuple
) -> None:
    try:
        iteration.generate_new_study_session(*session_data)
    except AttributeError:
        iteration.error_message = "ERROR: overlapping study sessions"
