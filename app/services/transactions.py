from utils.logger import logger
from app.db.connection import get_db


async def add_transaction(
    user_id: int,
    amount: int,
    type: str,
    category: str,
    date: str,
    description: str | None = None,
) -> None:

    db = get_db()
    db.execute(
        """
    INSERT INTO transactions (user_id, amount, type, category, description, date)
    VALUES (?, ?, ?, ?, ?, ?)
    """,
        (user_id, amount, type, category, description, date),
    )
    db.commit()
    logger.info("Creating a record in transactions")


async def get_transaction(
    user_id: int,
    amount: int,
    type: str,
    category: str,
    date: str,
    description: str | None = None,
) -> None:

    db = get_db()
    db.execute(
        """
    INSERT INTO transactions (user_id, amount, type, category, description, date)
    VALUES (?, ?, ?, ?, ?, ?)
    """,
        (user_id, amount, type, category, description, date),
    )
    db.commit()
    logger.info("Creating a record in transactions")

