import sqlite3


def get_db() -> sqlite3.Connection:
    with sqlite3.connect("database.db") as conn:
        conn.row_factory = sqlite3.Row  # Enables dict-like access
        return conn
