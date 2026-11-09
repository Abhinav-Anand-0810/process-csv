"""
Custom Exceptions for the project
"""

from enums import ErrorMessage


class ServiceBaseException(Exception):
    """
    Base Exception class for the service
    """

    def __init__(self, message: str | None = None):
        """
        Args:
            message: Error Message, if None a default message would be provided
        """

        self.message = message or ErrorMessage.ERROR_OCCURED.value
        super().__init__(self.message)


class NotFoundException(ServiceBaseException):
    """
    Exception for non-existing resource request
    """

    message = ErrorMessage.NOT_FOUND.value


class AlreadyExistsException(ServiceBaseException):
    """
    Exception for Already Existing Resource
    """

    message = ErrorMessage.ALREADY_EXISTS.value
