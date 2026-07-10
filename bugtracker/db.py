"""Database module – SQLite connection and initialisation."""

import sqlite3

DB_NAME = "bugs.db"


def get_connection():
    """Return a connection to the SQLite database with row_factory set."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the bugs table if it doesn't already exist."""
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS bugs (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT NOT NULL,
            description TEXT,
            status      TEXT DEFAULT 'open',
            priority    TEXT DEFAULT 'medium',
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    # Seed sample data if the table is empty
    count = conn.execute("SELECT COUNT(*) FROM bugs").fetchone()[0]
    if count == 0:
        conn.execute(
            "INSERT INTO bugs (title, description, status, priority) VALUES (?, ?, ?, ?)",
            ("Login button not working", "Clicking the login button on the homepage does nothing in Firefox.", "open", "high"),
        )
        conn.execute(
            "INSERT INTO bugs (title, description, status, priority) VALUES (?, ?, ?, ?)",
            ("Add dark mode toggle", "Users want a dark mode option in the settings menu.", "open", "medium"),
        )
        conn.execute(
            "INSERT INTO bugs (title, description, status, priority) VALUES (?, ?, ?, ?)",
            ("Fix typo on About page", "'Teh' should be 'The' in the first paragraph.", "in-progress", "low"),
        )
    conn.commit()
    conn.close()


def get_all_bugs(status=None, priority=None, search=None):
    """Return all bugs, optionally filtered, ordered by most recently created first."""
    conn = get_connection()
    query = "SELECT * FROM bugs WHERE 1=1"
    params = []

    if status:
        query += " AND status = ?"
        params.append(status)
    if priority:
        query += " AND priority = ?"
        params.append(priority)
    if search:
        query += " AND (title LIKE ? OR description LIKE ?)"
        like = f"%{search}%"
        params.extend([like, like])

    query += " ORDER BY created_at DESC"
    bugs = conn.execute(query, params).fetchall()
    conn.close()
    return bugs


def create_bug(title, description, priority="medium"):
    """Insert a new bug and return its id."""
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO bugs (title, description, priority) VALUES (?, ?, ?)",
        (title, description, priority),
    )
    conn.commit()
    bug_id = cursor.lastrowid
    conn.close()
    return bug_id


def get_bug(bug_id):
    """Return a single bug by its id."""
    conn = get_connection()
    bug = conn.execute(
        "SELECT * FROM bugs WHERE id = ?", (bug_id,)
    ).fetchone()
    conn.close()
    return bug


def update_bug(bug_id, title, description, status, priority):
    """Update an existing bug and set updated_at to now."""
    conn = get_connection()
    conn.execute(
        """
        UPDATE bugs
        SET title = ?,
            description = ?,
            status = ?,
            priority = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (title, description, status, priority, bug_id),
    )
    conn.commit()
    conn.close()


def delete_bug(bug_id):
    """Delete a bug by its id."""
    conn = get_connection()
    conn.execute("DELETE FROM bugs WHERE id = ?", (bug_id,))
    conn.commit()
    conn.close()
