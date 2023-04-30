from datetime import date
from flask import Flask, request, render_template, url_for, redirect
from committable import (
    get_context,
    record_study_session,
    open_new_iteration,
    close_current_iteration,
)

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        template_fields = ("count", "daterange", "weeks", "learning", "building")
        context = get_context(template_fields)
        if not context:
            return "No current iteration found"
        context["today"] = date.today().strftime("%Y-%m-%d")
        return render_template("tracker_page", **context)
    else:  # it's POST
        record_study_session(request.form)
        return redirect(url_for("index"))


@app.route("/open", methods=["GET", "POST"])
def open_iteration():
    if request.method == "GET":
        return render_template("open_new_i7n")
    else:  # it's POST
        open_new_iteration(request.form)
        return redirect(url_for("index"))


@app.route("/close", methods=["GET", "POST"])
def close_iteration():
    if request.method == "GET":
        return render_template("close_current_i7n")
    else:  # it's POST
        cannot_remove_current, cannot_write_new = close_current_iteration(request.form)
        return redirect(url_for("index"))
