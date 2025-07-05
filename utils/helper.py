import sqlite3
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from app.db.connection import get_db
from models.exceptions import AppBaseError
from utils.logger import logger
from models.app_base_response import AppBaseResponse


def get_user_info_by_email(email: str, key: str = None):

    try:
        db = get_db()
        query = db.execute("""SELECT * FROM users WHERE email = ?""", (email,))
        query_result = query.fetchone()

        if key is None:
            return query_result
        else:
            return query_result[key]

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


def handle_json_response(msg: str, http_code: status) -> JSONResponse:
    return JSONResponse(
        status_code=http_code,
        content=AppBaseResponse(message=msg, http_code=http_code).to_dict()
    )
