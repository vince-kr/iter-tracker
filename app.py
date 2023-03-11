from flask import Flask, render_template, request
from agile import Agile
from datetime import date

app = Flask(__name__)
progress_tracker = Agile()

@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "GET":
        it = progress_tracker.current_iteration
        it.todays_date = date.today()
        return render_template("tracker_page", iteration = it)
    else: # it's POST
        for key in request.form:
            print(key, request.form[key])

def addStudySessionToCurrentIteration(iteration:object, session_data:tuple) -> object:
    iteration.generateSession(*session_data)
    return iteration
