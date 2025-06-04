from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.routes import user, transactions
from models.app_base_response import AppBaseResponse
from models.exceptions import AppBaseError
from utils.logger import logger


app = FastAPI(
    title="Expense Tracker API",
    description="A simple API for tracking expenses.",
    # lifespan=lifespan,
)
app.include_router(user.router)
app.include_router(transactions.router)


# Global handler to tweak the response from HTTPException
@app.exception_handler(HTTPException)
async def override_http_exception(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content=exc.detail)


# Global handler for any unhandled cases
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error("Unhandled exception: %s", exc)  # full traceback in logs

    return JSONResponse(
        status_code=500,
        content=AppBaseResponse(
            message="Internal server error. Please try again later",
            http_code=500
        ).to_dict()
    )


# Global handler for AppBaseError to cover cases outside the route functions or middleware
@app.exception_handler(AppBaseError)
async def app_base_error_handler(request: Request, exc: AppBaseError) -> JSONResponse:
    logger.error(f"An application error has occurred: {exc.message}")
    return JSONResponse(
        status_code=exc.http_code,
        content=AppBaseResponse(
            message=exc.message,
            http_code=exc.http_code
        ).to_dict()
    )


# Global handler to tweak the response from RequestValidationError
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    new_format = [error for error in exc.errors()]

    if "not a valid email" in new_format[0]["msg"]:

        # For cases where the input email is invalid
        # The return msg is "An email address must have an @-sign."
        returned_msg = new_format[0]["msg"].split(": ")[1].rstrip(".")

        logger.error(f"Failed to validate the input data: {returned_msg}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=AppBaseResponse(message=returned_msg, http_code=400).to_dict(),
        )
    else:
        logger.error(f"Failed to validate the input data: {new_format[0]["msg"]}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=AppBaseResponse(
                message=new_format[0]["msg"], http_code=400
            ).to_dict(),
        )
