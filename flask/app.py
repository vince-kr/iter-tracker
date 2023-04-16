from datetime import date
from flask import Flask, request, render_template, url_for, redirect
from committable.committable import get_context, record_study_session

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        template_fields = ("count", "daterange", "weeks", "learning", "building")
        context = get_context(template_fields)
        context["today"] = date.today().strftime("%Y-%m-%d")
        return render_template("tracker_page", **context)
    else:  # it's POST
        record_study_session(request.form)
        return redirect(url_for("index"))
