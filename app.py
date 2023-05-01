from datetime import date
from flask import Flask, request, render_template, url_for, redirect
from committable import (
    live_iteration_exists,
    get_context,
    record_study_session,
    start_new_iteration,
    close_current_iteration,
)

app = Flask(__name__)


@app.route("/")
def index():
    if live_iteration_exists():
        return redirect(url_for("current_iteration"))
    else:
        return render_template("index")


@app.route("/live", methods=["GET", "POST"])
def current_iteration():
    if not live_iteration_exists():
        return redirect(url_for("start_iteration"))
    if request.method == "GET":
        template_fields = ("count", "daterange", "weeks", "learning", "building")
        context = get_context(template_fields)
        context["today"] = date.today().strftime("%Y-%m-%d")
        return render_template("tracker_page", **context)
    else:  # it's POST
        record_study_session(request.form)
        return redirect(url_for("current_iteration"))


@app.route("/new", methods=["GET", "POST"])
def start_iteration():
    if live_iteration_exists():
        return redirect(url_for("current_iteration"))
    if request.method == "GET":
        return render_template("open_new_i7n", today=date.today().strftime("%Y-%m-%d"))
    else:  # it's POST
        start_new_iteration(request.form)
        return redirect(url_for("current_iteration"))


@app.route("/close", methods=["GET", "POST"])
def close_iteration():
    if not live_iteration_exists():
        return render_template("index")
    if request.method == "GET":
        return render_template("close_current_i7n")
    else:  # it's POST
        errors = close_current_iteration(request.form)
        return redirect(url_for("index"))
