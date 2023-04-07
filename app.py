from flask import Flask, render_template
from agile import Iteration

app = Flask(__name__)


it = Iteration(
    5,
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


@app.route("/")
def index():
    context = {
        "weeks": [
            list(range(7)),
            list(range(7)),
        ],
    }
    context["count"] = it.count
    context["learning"] = it.learning
    context["building"] = it.building
    return render_template("tracker_page", **context)
