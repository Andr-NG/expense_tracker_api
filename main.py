from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.routes import user, transactions, categories
from models.exceptions import AppBaseError
from utils.logger import logger
from utils.helper import handle_json_response


app = FastAPI(
    title="Expense Tracker API",
    description="A simple API for tracking expenses.",
    # lifespan=lifespan,
)
app.include_router(user.router)
app.include_router(transactions.router)
app.include_router(categories.router)


# Global handler to tweak the response from HTTPException
@app.exception_handler(HTTPException)
async def override_http_exception(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content=exc.detail)


# Global handler for any unhandled cases
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error("Unhandled exception: %s", exc)  # full traceback in logs
    return handle_json_response(
        "Internal service error. Please try again later",
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


# Global handler for AppBaseError to cover cases outside the route functions or middleware
@app.exception_handler(AppBaseError)
async def app_base_error_handler(request: Request, exc: AppBaseError) -> JSONResponse:
    logger.error(f"An application error has occurred: {exc.message}")
    return handle_json_response(exc.message, exc.http_code)


# Global handler to tweak the response from HTTPException
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    new_format = [error for error in exc.errors()]

    if "not a valid email" in new_format[0]["msg"]:

        # For cases where the input email is invalid
        # The return msg is "An email address must have an @-sign."
        returned_msg = new_format[0]["msg"].split(": ")[1].rstrip(".")

        logger.error(f"Failed to validate the input data: {new_format[0]}")
        return handle_json_response(returned_msg, status.HTTP_400_BAD_REQUEST)

    elif new_format[0].get("type") == "value_error":
        new_format[0]["msg"] = f"Value error: {new_format[0]["ctx"]["error"]}"
        return handle_json_response(new_format[0]["msg"], status.HTTP_400_BAD_REQUEST)

    elif new_format[0].get("type") == "missing":
        if len(new_format) == 1:
            # Extracting a missing field from the generic response
            missing_field = new_format[0]["loc"][1]
            logger.error(
                f"Failed to validate the input data due to missing field: {missing_field}"
            )
            return handle_json_response(
                f"Missing required field: {missing_field}",
                status.HTTP_400_BAD_REQUEST,
            )
        else:
            # Extracting missing fields from the generic response
            missing_fields = [error["loc"][1] for error in new_format]
            logger.error(
                f"Failed to validate the input data due to missing fields: {missing_fields}"
            )
            return handle_json_response(
                f"Missing required fields: {', '.join(missing_fields)}",
                status.HTTP_400_BAD_REQUEST,
            )
    else:
        logger.error(f"Failed to validate the input data: {new_format}")
        return handle_json_response(new_format[0]["msg"], 400)
