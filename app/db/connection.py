import sqlite3
from utils.logger import logger


def get_db() -> sqlite3.Connection:
    with sqlite3.connect("database.db") as conn:
        conn.row_factory = sqlite3.Row  # Enables dict-like access
        return conn


db = get_db()
logger.info("Database instantiated")