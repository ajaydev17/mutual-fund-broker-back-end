from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status
from typing import Any, Callable

# create the exception classes below
class UserException(Exception):
    """
    Raised when the user already exists.
    """
    pass


class UserAlreadyExists(UserException):
    """
    Raised when the user already exists.
    """
    pass


class UserNotFound(UserException):
    """
    Raised when the user is not found.
    """
    pass


class InvalidCredentials(UserException):
    """
    Raised when the provided credentials are invalid.
    """
    pass


class InvalidToken(UserException):
    """
    Raised when the provided token is invalid.
    """
    pass


class AccessTokenRequired(UserException):
    """
    Raised when the user is not authenticated or provided refresh token instead of access token.
    """


class RefreshTokenRequired(UserException):
    """
    Raised when the user is not authenticated or provided access token instead of refresh token.
    """
    pass

class AccountNotVerified(UserException):
    """Account not yet verified"""
    pass


# create the exception classes below
class InvestmentException(Exception):
    """
    Raised when the user already exists.
    """
    pass


class InvestmentNotFound(InvestmentException):
    """
    Raised when the user already exists.
    """
    pass

class SchemeCodeAlreadyExists(InvestmentException):
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

    app.add_exception_handler(
        InvalidCredentials,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "Invalid credentials",
                "error_code": "invalid_credentials"
            }
        )
    )

    app.add_exception_handler(
        InvalidToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Invalid token",
                "resolution": "Please get a new token",
                "error_code": "invalid_token"
            }
        )
    )

    app.add_exception_handler(
        AccessTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Access token required",
                "resolution": "Please provide an access token",
                "error_code": "access_token_required"
            }
        )
    )

    app.add_exception_handler(
        RefreshTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Refresh token required",
                "resolution": "Please provide a refresh token",
                "error_code": "refresh_token_required"
            }
        )
    )

    app.add_exception_handler(
        UserNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "User not found",
                "error_code": "user_not_found"
            }
        )
    )

    app.add_exception_handler(
        AccountNotVerified,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Account Not verified",
                "error_code": "account_not_verified",
                "resolution": "Please check your email for verification details"
            },
        ),
    )

    app.add_exception_handler(
        InvestmentNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Investment not found",
                "error_code": "investment_not_found"
            }
        )
    )

    app.add_exception_handler(
        SchemeCodeAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Investment already exists for this scheme code",
                "error_code": "investment_already_exists_for_this_scheme_code"
            }
        )
    )