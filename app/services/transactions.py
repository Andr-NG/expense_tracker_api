import sqlite3
from typing import Any
from utils.logger import logger
from app.db.connection import db
from models import exceptions


async def add_transaction(
    user_id: int,
    amount: float,
    currency: str,
    type: str,
    category_id: int,
    transaction_id: str,
    date: str = None,
    description: str = None,
) -> None:

    try:
        # Checking the input category_id
        logger.info("Checking the input category_id for a given user in the database")
        query = db.execute(
            """
            SELECT categories.id, categories.type
            FROM users
            INNER JOIN categories ON categories.user_id = users.id
            WHERE users.id = ?
            """,
            (user_id,),
        )

        for cat in [dict(cat) for cat in query.fetchall()]:

            if category_id == cat["id"] and cat["type"] != type:
                logger.error(f"Input type: {type} is not equal to {cat["type"]}")
                raise exceptions.InvalidCategory(f"Type {type} does not match the actual category type", 404)  # noqa: E501

            elif category_id != cat["id"] and cat["type"] != type:
                logger.error(f"Type: {type} and category_id: {category_id} do not exist")
                raise exceptions.InvalidCategory(f"Type: {type} and category_id: {category_id} do not exist", 404)  # noqa: E501

            else:
                db.execute(
                    """
                INSERT INTO transactions (transaction_id, user_id, amount, currency, type, description, date,
                category_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,  # noqa: E501
                    (transaction_id, user_id, amount, currency, type, description, date, category_id),  # noqa: E501
                )
                db.commit()
                logger.info("Creating a record in transactions")
                break
    except sqlite3.Error as e:
        logger.error(f"A database error has occured when creating transactions: {e}")
        raise sqlite3.Error


async def get_transactions(
    user_id: str, category_id: int = None
) -> tuple[list[dict[Any, Any]], int]:
    try:
        if category_id is None:
            query = db.execute(
                """SELECT * FROM transactions WHERE user_id = ? """, (user_id,)
            )

        else:
            query = db.execute(
                """SELECT * FROM transactions WHERE user_id = ? and category_id = ? """,
                (user_id, category_id),
            )
        query_results = query.fetchall()
        trans = [dict(result) for result in query_results]
        return trans, len(trans)

    except sqlite3.Error as e:
        logger.error(f"A database error has occured when fetching transactions: {e}")
        raise sqlite3.Error


async def delete_transaction(user_id: str, trans_id: str) -> list[dict[str, Any]]:
    try:
        # Veryfing the transaction_id sent
        query = db.execute(
            """
            DELETE FROM transactions as t
            WHERE t.transaction_id = ? and t.user_id = ?
            """,
            (trans_id, user_id),
        )
        if query.rowcount == 0:
            logger.error("Transaction not found or not owned by user")
            raise exceptions.TransactionNotFound(
                "Transaction not found or not owned by user", 404
            )

    except sqlite3.Error as e:
        logger.error(f"A database error has occured when deleing transactions: {e}")
        raise sqlite3.Error
