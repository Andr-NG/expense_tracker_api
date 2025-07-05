import sqlite3
from utils.logger import logger
from app.db.connection import db


default_expense = [
    "groceries",
    "rent",
    "utilities",
    "transportation",
    "subscriptions",
    "entertainment",
    "other",
]
default_income = ["salary", "freelance", "reimbursement", "other"]
types = ["income", "expense"]


async def fetch_categories(email: str) -> list:
    try:
        query = db.execute(
            """SELECT categories.id, categories.type, categories.name, categories.description
               FROM users
               INNER JOIN categories ON users.id = categories.user_id
               WHERE users.email = ?
            """,
            (email,),
        )
        lst = [dict(category) for category in query.fetchall()]
        return lst

    except sqlite3.Error as e:
        logger.error(
            f"A database error has occurred when listing categories for the db: {e}"
        )
        raise sqlite3.Error


async def create_default_categories(user_id: int) -> None:
    try:
        for type in types:
            if type == "expense":
                for expense in default_expense:
                    db.execute(
                        """ INSERT INTO categories (user_id, name, type, description)
                            VALUES (?, ?, ?, ?)
                        """,
                        (user_id, expense, type, "default category"),
                    )
            else:
                for income in default_income:
                    db.execute(
                        """ INSERT INTO categories (user_id, name, type, description)
                            VALUES (?, ?, ?, ?)
                        """,
                        (user_id, income, type, "default category"),
                    )
    except sqlite3.Error as e:
        logger.error(
            f"A database error has occured when creating default categories: {e}"
        )
        raise sqlite3.Error
    finally:
        db.commit()
