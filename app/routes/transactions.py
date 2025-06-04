from utils.dependencies import verify_token
from fastapi.params import Depends
from utils.logger import logger
from fastapi import APIRouter, HTTPException, status
from models import AppBaseResponse, CreateTransaction
from app.services.transactions import add_transaction
from models.exceptions import AppBaseError
from utils.helper import handle_app_exception, handle_db_exception
import models
import sqlite3

router = APIRouter(prefix="/api/v1/transactions", tags=["Transactions"])


@router.post(
    "/add", response_model=AppBaseResponse, status_code=status.HTTP_201_CREATED
)
async def create_new_transaction(
    trans: CreateTransaction, user_token: models.UserToken = Depends(verify_token)
) -> AppBaseResponse:
    try:
        if user_token.user_id:
            await add_transaction(
                user_id=user_token.user_id,
                amount=trans.amount,
                date=trans.date,
                category=trans.category,
                type=trans.type,
                description=trans.description,
            )
        return AppBaseResponse(
            message="Transaction added successfully", http_code=status.HTTP_201_CREATED
        )

    except AttributeError as e:
        logger.error(f"An attribute error has occurred: {e}")
        raise HTTPException(
            status_code=401,
            detail=AppBaseResponse(message="Invalid JWT", http_code=401).to_dict(),
        )

    except AppBaseError as e:
        logger.error(f"An app error has occurred: {e}")
        raise handle_app_exception(e)

    except sqlite3.Error as e:
        logger.error(f"A database error has occurred: {e}")
        raise handle_db_exception()
