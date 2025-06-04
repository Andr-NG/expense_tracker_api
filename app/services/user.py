import hashlib
import os
import re
import jwt
from datetime import datetime, timedelta
from models import exceptions
from utils.logger import logger
from app.db.connection import get_db


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


async def create_user(email: str, password: str) -> None:

    if not bool(re.fullmatch(r"^(?=.*[@$!%*?&]).{6,}$", password)):
        raise ValueError(
            "Password must include at least one special character [@$!%*?&]"
        )

    db = get_db()
    query = db.execute(
        """SELECT email FROM users WHERE email = ?""",
        (email.lower(),),
    )
    query_result = query.fetchone()

    if not query_result:
        hashed = hash_password(password)
        db.execute(
            """INSERT INTO users (email, hashed_password) VALUES (?, ?)""",
            (email.lower(), hashed),
        )
        db.commit()

    elif query_result["email"] == email.lower():
        raise exceptions.EmailAlreadyExists(
            f"User with email '{email.lower()}' already exists", 409
        )


async def sign_in(password: str, email: str = None) -> str:

    db = get_db()
    query = db.execute(
        """SELECT id, email, hashed_password, is_active FROM users WHERE email = ?""",
        (email,),
    )
    query_result = query.fetchone()
    logger.info("Fetching all the user details from the database by email")

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
            return token
        else:
            logger.error("Failed to verify the input user password. Wrong password")
            raise exceptions.WrongPassword("Wrong user password", 401)
