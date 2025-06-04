from fastapi import Header
from utils.logger import logger
from models import exceptions
from models import UserToken
import os
import models
import jwt


def verify_token(authorization: str = Header(...)) -> UserToken | None:
    """Verifying the token

        Args:
            authorization (str): token

        Returns:
            dict
    """
    try:
        token = authorization.split()[1]
        logger.info("Decoding the user token: %s", token)
        decoded = jwt.decode(jwt=token, key=os.getenv("SECRET"), algorithms="HS256")
        decoded_jwt = models.UserToken(**decoded)
        logger.info(f"token is {decoded_jwt}")
        return decoded_jwt

    except jwt.exceptions.ExpiredSignatureError as e:
        logger.error("Failed to decode the user token: %s", e)
        raise exceptions.WrongToken("User token expired", 401)

    except jwt.DecodeError as e:
        logger.error("Failed to decode the user token: %s", e)
        raise exceptions.WrongToken("Invalid JWT", 401)
