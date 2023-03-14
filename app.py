from flask import Flask, render_template, request, redirect, url_for
from agile import Agile
from datetime import date

app = Flask(__name__)
a = Agile()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        a.current_iteration.todays_date = date.today()
        return render_template("tracker_page", iteration=a.current_iteration)
    else:  # it's POST
        date_of_session = date.fromisoformat(request.form["session_date"])
        session_data = (
            date_of_session,
            request.form["goal_type"],
            request.form["start_time"],
            request.form["end_time"]
        )
        add_study_session_to_current_iteration(a.current_iteration, session_data)
        return redirect(url_for("index"))


def add_study_session_to_current_iteration(iteration: object, session_data: tuple) -> object:
    try:
        iteration.generate_session(*session_data)
    except AttributeError:
        iteration.error_message = "ERROR: overlapping study sessions"
    return iteration
