from flask import Flask, request, render_template, url_for, redirect
from datetime import date
from agile import iteration_factory

app = Flask(__name__)


it = iteration_factory()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        context = {
            "count": it.count,
            "daterange": it.daterange,
            "weeks": it.weeks,
            "learning": it.learning,
            "building": it.building,
        }
        return render_template("tracker_page", **context)
    else:  # it's POST
        session_data = (
            request.form["date"],
            request.form["goal_type"],
            request.form["start_time"],
            request.form["end_time"],
        )
        record_study_session(session_data, it)
        return redirect(url_for("index"))


def record_study_session(session_data: tuple, iteration: object) -> None:
    iteration.record_study_session(*session_data)
