from flask import Flask, request, render_template, url_for, redirect
from committable import get_context

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        template_fields = ("count", "daterange", "weeks", "learning", "building")
        context = get_context(template_fields)
        return render_template("tracker_page", **context)
    else:  # it's POST
        session_data = (
            request.form["date"],
            request.form["goal_type"],
            request.form["start_time"],
            request.form["end_time"],
        )
        record_study_session(it, session_data)
        return redirect(url_for("index"))


def record_study_session(iteration: object, session_data: tuple) -> None:
    iteration.record_study_session(*session_data)
