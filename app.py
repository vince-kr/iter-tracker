from flask import Flask, request, render_template, url_for, redirect
from datetime import date
from agile import Iteration

app = Flask(__name__)


it = Iteration(
    5,
    date.fromisoformat("2023-04-01"),
    (
        "3hrs studying Fluent Python (at least finish ch.5, which is 30 more pages); 1hr practicing TCR.",
        240,
        0,
    ),
    (
        "I want to implement showing the progress on an iteration in terms of percentage of the time goal versus how much of the iteration has passed. I also want to keep working on the note transposing problem. Say 3hrs for Iteration-Tracker and 1hr on music.",
        270,
        0,
    ),
)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        context = {
            "count": it.count,
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
