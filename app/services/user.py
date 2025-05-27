import hashlib
import os
import re
import jwt
from datetime import datetime, timedelta, timezone
from models import exceptions
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

    now = datetime.now(tz=timezone.utc)
    claimset = {"email": email.lower(), "iat": now, "exp": now + timedelta(days=1)}
    md5_hashed = hashlib.sha256(password.encode()).hexdigest()

    db = get_db()
    query = db.execute(
        """SELECT email, hashed_password FROM users WHERE email = ?""", (email,)
    )
    query_result = query.fetchone()

    if not query_result:
        raise exceptions.UserNotFound("User not found", 404)

    if all(
        [
            query_result["email"] == email,
            query_result["hashed_password"] == md5_hashed,
        ]
    ):
        token = jwt.encode(payload=claimset, key=os.getenv("SECRET"), algorithm="HS256")
        return token
    else:
        raise exceptions.WrongPassword("Wrong password", 401)
