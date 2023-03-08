from flask import Flask, render_template
from agile import Agile

app = Flask(__name__)
progress_tracker = Agile()

@app.route("/")
def index():
    it = progress_tracker.current_iteration
    return render_template("tracker_page", iteration = it)
