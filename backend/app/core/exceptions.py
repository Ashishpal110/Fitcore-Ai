from typing import Any, Dict, Optional


class FitCoreException(Exception):
    """Base exception for all domain and application errors."""

    def __init__(
        self,
        message: str,
        status_code: int = 400,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)


class NotFoundException(FitCoreException):
    def __init__(self, resource: str, identifier: Any):
        super().__init__(
            message=f"{resource} with identifier '{identifier}' was not found.",
            status_code=404,
            details={"resource": resource, "identifier": str(identifier)},
        )


class UnauthorizedException(FitCoreException):
    def __init__(self, message: str = "Authentication required"):
        super().__init__(message=message, status_code=401)


class ForbiddenException(FitCoreException):
    def __init__(self, message: str = "Access forbidden"):
        super().__init__(message=message, status_code=403)


class ConflictException(FitCoreException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=409, details=details)


class ValidationException(FitCoreException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=422, details=details)
