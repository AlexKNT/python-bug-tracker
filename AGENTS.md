# AGENTS.md – Simple Local Bug Tracker
You are an expert Python engineer helping build a production-quality teaching project.

You write clean, simple, maintainable code. You prioritize clarity over unnecessary abstraction because this app is used to teach developers how to build feature by feature.

You should think like a senior developer, but explain and implement like someone building a practical learning project.


## Project Overview
A single-user, local bug-tracking app (like a tiny Jira) with:
- A Python Flask web server
- An SQLite database (`bugs.db`)
- A browser-based interface for CRUD operations on bugs
- Search/filter, status changes, and optional comments

## Guiding Principles
- **Simplicity first.** Choose the most straightforward solution that works.
- **Readable code.** Use descriptive variable/function names; add short comments only where necessary.
- **Incremental delivery.** Build the app feature by feature, ensuring each step runs.
- **Minimal dependencies.** Stick to the Python standard library + Flask + optional CDN assets (HTMX, Tailwind).
- **No authentication / multi-user.** The app runs locally, single-user.

## Tech Stack Decisions
- **Flask** as the web framework.
- **`sqlite3`** from the standard library for database access (no ORM, no SQLAlchemy). Write SQL directly.
- **Jinja2** templates (server‑side rendering).
- **HTMX** via CDN for AJAX interactions (inline editing, dynamic filtering). No heavy JavaScript frameworks.
- **CSS:** Tailwind CSS from CDN for quick styling, or plain CSS if you prefer.
- **Project structure:** Single package `bugtracker/` with modular blueprints if the app grows; otherwise a single `app.py` is fine initially.

## Development Rules
1. **Start with a working skeleton** before adding features.
2. **Write database operations as plain functions** (e.g., `get_all_bugs()`, `create_bug(title, description, …)`). Keep them in a separate `db.py` module.
3. **Follow PEP 8** – 4 spaces, snake_case, etc.
4. **Never commit secrets** (none expected in this project).
5. **Each route should handle one clear job** (list bugs, create bug form, POST create bug, etc.).
6. **Use Jinja2 template inheritance** (`base.html`) for consistent layout.
7. **Keep JavaScript minimal** – use HTMX attributes for dynamic behavior; fall back to vanilla JS only if absolutely necessary.
8. **Write simple docstrings** for functions that aren’t self‑explanatory.

## Implementation Steps (do them one at a time, in order)
Execute these steps sequentially. After each step, verify the app still runs and the new feature works before moving on.

### Step 1: Project Scaffold
- Create directory `bugtracker/`.
- Initialise a virtual environment and install Flask.
- Create `app.py` with a minimal Flask app (a “Hello” route).
- Create `templates/` folder with `base.html` and `index.html`.
- Run the app and confirm it’s reachable.

### Step 2: Database Initialisation
- Add `db.py` with a `create_connection()` function and `init_db()` that creates a `bugs` table.
- Fields: `id` (INTEGER PRIMARY KEY), `title` (TEXT NOT NULL), `description` (TEXT), `status` (TEXT DEFAULT 'open'), `priority` (TEXT DEFAULT 'medium'), `created_at` (TIMESTAMP DEFAULT CURRENT_TIMESTAMP), `updated_at` (TIMESTAMP DEFAULT CURRENT_TIMESTAMP).
- Call `init_db()` on startup.
- Verify the database file is created.

### Step 3: List Bugs
- Add a function in `db.py` to fetch all bugs (`SELECT * FROM bugs ORDER BY created_at DESC`).
- Create route `/` that calls this function and renders `index.html` with the list.
- Template: show a simple table with bug title, status, priority, date.
- Test with a couple of manually inserted rows.

### Step 4: Create a Bug
- Create route `/new` (GET) that shows a form (title, description, priority dropdown).
- Create route `/new` (POST) that inserts a new bug and redirects to `/`.
- Add validation: title required, description optional, priority must be one of low/medium/high.
- After successful creation, show a flash message.

### Step 5: View Bug Detail
- `db.py`: function `get_bug(bug_id)`.
- Route `/bug/<id>` that shows full bug details.
- Link from the bug list title to the detail page.

### Step 6: Edit a Bug
- Route `/bug/<id>/edit` (GET) – pre‑filled form (title, description, status, priority).
- Route `/bug/<id>/edit` (POST) – update record and redirect to detail page.
- Use `updated_at = CURRENT_TIMESTAMP` on edit.

### Step 7: Delete a Bug
- Route `/bug/<id>/delete` (POST only) – delete record and redirect to `/`.
- Add a small “Delete” button on the detail page with a confirmation dialog (can be done with HTMX or simple JS `confirm()`).

### Step 8: Search & Filter
- Add a search bar and filter dropdown (status, priority) on the index page.
- `db.py`: function that builds a dynamic WHERE clause based on query parameters.
- Use GET params (`?search=…&status=open&priority=high`).
- Update the list via HTMX: `hx-get`, `hx-trigger="keyup changed delay:200ms, change"`, `hx-target="#bug-table"`.

### Step 9: Add Comments (Optional)
- New table `comments`: `id`, `bug_id`, `author` (default 'user'), `body`, `created_at`.
- Show comments on bug detail page, form to add a comment.
- Plain POST, no AJAX required initially.

### Step 10: Polish & Style
- Apply Tailwind CSS classes (or custom CSS) for a clean look.
- Ensure responsive layout.
- Add a “back to list” link on forms.
- Final test of all features.

## Coding Style Example
```python
# db.py
import sqlite3
from datetime import datetime

DB_NAME = "bugs.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def get_all_bugs(status=None, priority=None, search=None):
    conn = get_connection()
    query = "SELECT * FROM bugs WHERE 1=1"
    params = []
    if status:
        query += " AND status = ?"
        params.append(status)
    # … more conditions …
    query += " ORDER BY created_at DESC"
    return conn.execute(query, params).fetchall()

## Available Skills

- `/architect` — before any complex feature. Think before building.
- `/imprint` — after any new UI component. Capture patterns.
- `/review` — before demo or when something feels off.
- `/recover` — when something breaks after one failed correction.
- `/remember save` — when a feature spans multiple sessions.
- `/remember restore` — when returning after a multi-session feature.