"""Simple Local Bug Tracker – Flask application."""

from flask import Flask, flash, redirect, render_template, request, url_for

from db import create_bug, get_all_bugs, get_bug, init_db, update_bug

app = Flask(__name__)
app.secret_key = "dev-secret-key"

# Initialise the database on startup
init_db()


@app.route("/")
def index():
    """Home page – list all bugs."""
    bugs = get_all_bugs()
    return render_template("index.html", bugs=bugs)


@app.route("/new", methods=["GET", "POST"])
def new_bug():
    """Create a new bug – show form (GET) or handle submission (POST)."""
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        priority = request.form.get("priority", "medium")

        # Validation
        errors = []
        if not title:
            errors.append("Title is required.")
        if priority not in ("low", "medium", "high"):
            errors.append("Priority must be low, medium, or high.")

        if errors:
            for error in errors:
                flash(error, "error")
            return render_template(
                "new_bug.html",
                title=title,
                description=description,
                priority=priority,
            ), 400

        create_bug(title, description, priority)
        flash("Bug created successfully!", "success")
        return redirect(url_for("index"))

    return render_template("new_bug.html")


@app.route("/bug/<int:bug_id>")
def bug_detail(bug_id):
    """Show full details for a single bug."""
    bug = get_bug(bug_id)
    if bug is None:
        flash("Bug not found.", "error")
        return redirect(url_for("index"))
    return render_template("bug_detail.html", bug=bug)


@app.route("/bug/<int:bug_id>/edit", methods=["GET", "POST"])
def edit_bug(bug_id):
    """Edit a bug – show pre-filled form (GET) or handle update (POST)."""
    bug = get_bug(bug_id)
    if bug is None:
        flash("Bug not found.", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        status = request.form.get("status", "open")
        priority = request.form.get("priority", "medium")

        # Validation
        errors = []
        if not title:
            errors.append("Title is required.")
        if status not in ("open", "in-progress", "closed"):
            errors.append("Status must be open, in-progress, or closed.")
        if priority not in ("low", "medium", "high"):
            errors.append("Priority must be low, medium, or high.")

        if errors:
            for error in errors:
                flash(error, "error")
            return render_template(
                "edit_bug.html",
                bug=bug,
                title=title,
                description=description,
                status=status,
                priority=priority,
            ), 400

        update_bug(bug_id, title, description, status, priority)
        flash("Bug updated successfully!", "success")
        return redirect(url_for("bug_detail", bug_id=bug_id))

    return render_template("edit_bug.html", bug=bug)


if __name__ == "__main__":
    app.run(debug=True)
