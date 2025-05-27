import sqlite3
from fastapi import APIRouter, HTTPException, status
from models import AppBaseResponse, UserCreate
from app.services.user import create_user, sign_in
from models.exceptions import AppBaseError
from models.sign_in_response import SignInResponse
from models.user_sign_in import UserSignIn

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
        raise HTTPException(
            status_code=409,
            detail=AppBaseResponse(message=e.message, http_code=e.http_code).to_dict(),
        )
    except sqlite3.DatabaseError:
        raise HTTPException(
            status_code=409,
            detail=AppBaseResponse(
                message="Database issue has occurred", http_code=409
            ).to_dict(),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=AppBaseResponse(message=str(e), http_code=400).to_dict(),
        )


@router.post("/login", response_model=SignInResponse, status_code=status.HTTP_200_OK)
async def log_in(user: UserSignIn) -> SignInResponse:

    try:
        token = await sign_in(password=user.password, email=user.email)
        return SignInResponse(
            message="User signed in successfully",
            token=token,
            http_code=status.HTTP_201_CREATED,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=AppBaseResponse(message=str(e), http_code=400).to_dict(),
        )
