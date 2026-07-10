"""Simple Local Bug Tracker – Flask application."""

from flask import Flask, render_template

from db import get_all_bugs, init_db

app = Flask(__name__)
app.secret_key = "dev-secret-key"

# Initialise the database on startup
init_db()


@app.route("/")
def index():
    """Home page – list all bugs."""
    bugs = get_all_bugs()
    return render_template("index.html", bugs=bugs)


if __name__ == "__main__":
    app.run(debug=True)
