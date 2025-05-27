class AppBaseError(Exception):
    """Base exception for all application-specific errors."""
    def __init__(self, message: str, http_code: int) -> None:
        self.message = message
        self.http_code = http_code
        super().__init__(message)


class EmailAlreadyExists(AppBaseError):
    """Raised when a user with the given email already exists."""

