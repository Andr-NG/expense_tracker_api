import hashlib
import os
import re
import sqlite3
import jwt
from datetime import datetime, timedelta
from models import exceptions
from utils.logger import logger
from app.db.connection import db
from utils.helper import get_user_info_by_email
from app.services.categories import create_default_categories


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


async def create_user(email: str, password: str) -> None:

    if not bool(re.fullmatch(r"^(?=.*[@$!%*?&]).{6,}$", password)):
        raise ValueError(
            "Password must include at least one special character [@$!%*?&]"
        )
    try:
        query = db.execute(
            """SELECT email FROM users WHERE email = ?""",
            (email.lower(),),
        )
        query_result = query.fetchone()
    except sqlite3.Error as e:
        logger.error(f"A database error has occurred when checking the user email in the db: {e}")
        raise sqlite3.Error

    # Checking whether the email exists or not
    if not query_result:
        hashed = hash_password(password)
        db.execute(
            """INSERT INTO users (email, hashed_password) VALUES (?, ?)""",
            (email.lower(), hashed),
        )
        db.commit()
        logger.info(f"New user with email {email} created successfully")

        # Getting user_id to create default categories
        id = get_user_info_by_email(email.lower(), "id")
        await create_default_categories(user_id=id)
        logger.info(f"Default categories created for user_id: {id}")

    elif query_result["email"] == email.lower():
        raise exceptions.EmailAlreadyExists(
            f"User with email '{email.lower()}' already exists", 409
        )


async def sign_in(password: str, email: str = None) -> str:

    try:
        query_result = get_user_info_by_email(email)
        logger.info("Fetching all the user details from the database by email")

    except sqlite3.Error as e:
        logger.error(f"A database error has occurred when fetching user details: {e}")
        raise sqlite3.Error

    if not query_result:
        logger.error("Failed to find the user email in the database")
        raise exceptions.UserNotFound("User email not found", 404)

    logger.info("User credentials fetched from the database. Verifying the account status")
    if not query_result["is_active"]:
        logger.error("User's account is deactivated")
        raise exceptions.SuspendedAccount("Account deactivated", 401)

    else:
        logger.info("User account verified")
        md5_hashed = hashlib.sha256(password.encode()).hexdigest()
        logger.info("Veryfing the input credentials")
        if all(
            [
                query_result["email"] == email,
                query_result["hashed_password"] == md5_hashed,
            ]
        ):
            now = datetime.now()
            claimset = {
                "email": email.lower(),
                "user_id": query_result["id"],
                "is_active": bool(query_result["is_active"]),
                "iat": round(now.timestamp()),
                "exp": round((now + timedelta(hours=2)).timestamp()),
            }
            token = jwt.encode(
                payload=claimset, key=os.getenv("SECRET"), algorithm="HS256"
            )
            logger.info("Returning the user's token")
            return token, query_result["id"]
        else:
            logger.error("Failed to verify the input user password. Wrong password")
            raise exceptions.WrongPassword("Wrong user password", 401)
