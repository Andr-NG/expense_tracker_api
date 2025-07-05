import sqlite3
from fastapi import APIRouter, status
from fastapi.params import Depends
from app.services.categories import fetch_categories
from models.get_categories_response import GetCategoriesResponse
from models.exceptions import AppBaseError
from utils.dependencies import verify_token
from utils.helper import handle_db_exception, handle_app_exception
from utils.logger import logger
import models


router = APIRouter(prefix="/api/v1/categories", tags=["Categories"])


@router.get(
    "/",
    response_model=GetCategoriesResponse,
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
async def get_categories(
    user_token: models.UserToken = Depends(verify_token),
) -> GetCategoriesResponse:
    try:
        if user_token.email:
            logger.info(f"Fetching categories for user_id {user_token.email}")
            categories = await fetch_categories(user_token.email)

            return GetCategoriesResponse(
                message="Categories fetched successfully",
                http_code=status.HTTP_200_OK,
                data=categories,
            )

    except AppBaseError as e:
        logger.error(f"An app error has occurred: {e}")
        raise handle_app_exception(e)

    except sqlite3.Error:
        raise handle_db_exception()
