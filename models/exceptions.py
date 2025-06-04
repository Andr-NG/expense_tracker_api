class AppBaseError(Exception):
    """Base exception for all application-specific errors."""

    def __init__(self, message: str, http_code: int) -> None:
        self.message = message
        self.http_code = http_code
        super().__init__(message)


class EmailAlreadyExists(AppBaseError):
    """Raised when a user with the given email already exists."""


class UserNotFound(AppBaseError):
    """Raised when the given email does not exist."""


class WrongPassword(AppBaseError):
    """Raised when the given password does not exist."""


class SuspendedAccount(AppBaseError):
    """Raised when is_active=False"""


class WrongToken(AppBaseError):
    """Raised when JWT is invalid"""


class DataBaseError(AppBaseError):
    """Raised when  there a db error"""
