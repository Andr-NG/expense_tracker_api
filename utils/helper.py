import sqlite3
from fastapi import HTTPException
from app.db.connection import get_db
from models.exceptions import AppBaseError
from utils.logger import logger
from models.app_base_response import AppBaseResponse


def get_user_info_by_email(email: str):
    try:
        db = get_db()
        query = db.execute("""SELECT * FROM users WHERE email = ?""", (email,))
        query_result = query.fetchone()
        logger.info("Fetching all the user details from the database by email")
        return query_result
    except sqlite3.DatabaseError as e:
        logger.error("Failed to fetch the user info: %s", e)
        raise
    except Exception as e:
        logger.error("An uknown error occured when retrieving user info: %s", e)
        raise


def handle_app_exception(exc: AppBaseError) -> HTTPException:
    return HTTPException(
        status_code=exc.http_code,
        detail=AppBaseResponse(message=exc.message, http_code=exc.http_code).to_dict(),
    )


def handle_db_exception() -> HTTPException:
    return HTTPException(
        status_code=500,
        detail=AppBaseResponse(
            message="Internal database error", http_code=500
        ).to_dict(),
    )

# def handle_db_exception(exc: Exception) -> HTTPException:
#     return HTTPException(
#         status_code=500,
#         detail=AppBaseResponse(
#             message="Database error: " + str(exc),
#             http_code=500
#         ).to_dict()
#     )