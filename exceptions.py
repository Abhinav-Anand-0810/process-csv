"""
Custom Exceptions for the project
"""

from enums import ErrorMessage


class TaskBaseException(Exception):
    """
    Base Exception class for the service
    """

    default_error_message: str = ErrorMessage.ERROR_OCCURED.value

    def __init__(self, message: str | None = None):
        """
        Args:
            message: Error Message, if None a default message would be provided
        """

        self.message = message or self.default_error_message
        super().__init__(self.message)


class NotFoundException(TaskBaseException):
    """
    Exception for non-existing resource request
    """

    default_error_message = ErrorMessage.NOT_FOUND.value


class AlreadyExistsException(TaskBaseException):
    """
    Exception for Already Existing Resource
    """

    default_error_message = ErrorMessage.ALREADY_EXISTS.value
