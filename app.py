from flask import Flask, render_template, request, redirect, url_for
from agile import Agile
from datetime import date

app = Flask(__name__)
a = Agile()


@app.route("/", methods=["GET", "POST"])
def index():
    iteration = a.current_iteration
    if request.method == "GET":
        context = {
            "todays_date": date.today(),
            "counter": iteration.counter,
            "start_to_end": iteration.start_to_end,
            "weeks": iteration.weeks,
            "study_sessions": iteration.study_sessions,
            "goals": iteration.goals,
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
