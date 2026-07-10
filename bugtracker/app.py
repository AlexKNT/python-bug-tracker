"""Simple Local Bug Tracker – Flask application."""

from flask import Flask, render_template

from db import init_db

app = Flask(__name__)
app.secret_key = "dev-secret-key"

# Initialise the database on startup
init_db()


@app.route("/")
def index():
    """Home page – will list all bugs."""
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
