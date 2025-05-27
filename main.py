from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.routes import user
from models.app_base_response import AppBaseResponse

app = FastAPI(
    title="Expense Tracker API", description="A simple API for tracking expenses."
)


@app.exception_handler(HTTPException)
async def override_http_exception(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content=exc.detail)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    new_format = [error for error in exc.errors()]

    if "not a valid email" in new_format[0]["msg"]:

        # For cases where the input email is invalid
        # The return msg is "An email address must have an @-sign."
        returned_msg = new_format[0]["msg"].split(": ")[1].rstrip('.')

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=AppBaseResponse(
                message=returned_msg, http_code=400
            ).to_dict()
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=AppBaseResponse(
                message=new_format[0]["msg"], http_code=400
            ).to_dict(),
        )


app.include_router(user.router)
