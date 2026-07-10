"""Simple Local Bug Tracker – Flask application."""

from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = "dev-secret-key"


@app.route("/")
def index():
    """Home page – will list all bugs."""
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
