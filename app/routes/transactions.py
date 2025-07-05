from app.services.transactions import add_transaction, get_transactions, delete_transaction
from fastapi.params import Depends
from fastapi import APIRouter, HTTPException, Query, status
from models.get_transactions_response import GetTransactionsResponse
from models.exceptions import AppBaseError
from models import AppBaseResponse, Transaction
from utils.dependencies import verify_token
from utils.logger import logger
from utils.helper import handle_app_exception, handle_db_exception
import models
import sqlite3
import shortuuid

router = APIRouter(prefix="/api/v1/transactions", tags=["Transactions"])


@router.get(
    "/",
    response_model=GetTransactionsResponse,
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
async def fetch_transactions_by_user(
    user_token: models.UserToken = Depends(verify_token),
    limit: int = Query(default=None, gt=0),
    category_id: int | None = Query(default=None, gt=0),
) -> GetTransactionsResponse:
    try:
        if user_token.user_id:
            logger.info(f"Fetching transactions for user_id {user_token.user_id}")
            trans, count = await get_transactions(user_token.user_id, category_id=category_id)
        return GetTransactionsResponse(
            message="Transactions fetched successfully",
            http_code=status.HTTP_200_OK,
            data=trans[:limit],
            count=count
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


@router.post(
    "/add", response_model=AppBaseResponse, status_code=status.HTTP_201_CREATED
)
async def create_new_transaction(
    trans: Transaction, user_token: models.UserToken = Depends(verify_token)
) -> AppBaseResponse:
    try:
        if user_token.user_id:
            await add_transaction(
                transaction_id=str(shortuuid.uuid()),
                user_id=user_token.user_id,
                amount=trans.amount,
                date=trans.date,
                category_id=trans.category_id,
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

    except sqlite3.Error:
        raise handle_db_exception()


@router.delete(
    "/delete/{id}",
    response_model=AppBaseResponse,
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
async def remove_transaction(
    id: str,
    user_token: models.UserToken = Depends(verify_token),
) -> AppBaseResponse:
    try:
        if user_token.user_id:
            await delete_transaction(user_token.user_id, id)
        return AppBaseResponse(
            message="Transaction removed successfully",
            http_code=status.HTTP_200_OK,
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
