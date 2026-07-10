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


def get_all_bugs():
    """Return all bugs ordered by most recently created first."""
    conn = get_connection()
    bugs = conn.execute(
        "SELECT * FROM bugs ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return bugs
