import sqlite3
from utils.logger import logger
from fastapi import APIRouter, HTTPException, status
from models import AppBaseResponse, UserCreate
from app.services.user import create_user, sign_in
from models.exceptions import AppBaseError
from models.sign_in_response import SignInResponse
from models.user_sign_in import UserSignIn
from utils.helper import handle_app_exception, handle_db_exception

router = APIRouter(prefix="/api/v1/user", tags=["User"])


@router.post(
    "/register", response_model=AppBaseResponse, status_code=status.HTTP_201_CREATED
)
async def register(user: UserCreate) -> AppBaseResponse:

    try:
        await create_user(user.email, user.password)
        return AppBaseResponse(
            message="User created successfully", http_code=status.HTTP_201_CREATED
        )
    except AppBaseError as e:
        logger.error(f"An app error has occurred: {e}")
        raise handle_app_exception(e)

    except sqlite3.Error as e:
        logger.error(f"A database error has occurred: {e}")
        raise handle_db_exception()

    # Handling the password error
    except ValueError as e:
        logger.error(f"A value error has occurred: {e}")
        raise HTTPException(
            status_code=400,
            detail=AppBaseResponse(message=str(e), http_code=400).to_dict(),
        )


@router.post("/login", response_model=SignInResponse, status_code=status.HTTP_200_OK)
async def log_in(user: UserSignIn) -> SignInResponse:

    try:
        logger.info("Attempting to sign in")
        token = await sign_in(password=user.password, email=user.email)
        logger.info("User signed in successfully")
        return SignInResponse(
            message="User signed in successfully",
            token=token,
            http_code=status.HTTP_201_CREATED,
        )

    except AppBaseError as e:
        logger.error(f"An app error has occurred: {e}")
        raise HTTPException(
            status_code=e.http_code,
            detail=AppBaseResponse(message=e.message, http_code=e.http_code).to_dict(),
        )

    except sqlite3.Error as e:
        logger.error(f"A database error has occurred: {e}")
        raise handle_db_exception()
