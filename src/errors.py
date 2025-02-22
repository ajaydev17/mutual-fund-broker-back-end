from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status
from typing import Any, Callable

# create the exception classes below
class UserAlreadyExists(Exception):
    """
    Raised when the user already exists.
    """
    pass


# create the exception handler below
def create_exception_handler(status_code: int,
                             initial_detail: Any) -> Callable[[Request, Exception], JSONResponse]:
    async def exception_handler(request: Request, exc: UserAlreadyExists):
        return JSONResponse(
            content=initial_detail,
            status_code=status_code
        )

    return exception_handler


# register all exceptions
def register_all_exceptions(app: FastAPI):
    app.add_exception_handler(
        UserAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "User with email already exists",
                "error_code": "user_exists"
            }
        )
    )