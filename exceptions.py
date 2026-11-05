"""
Custom Exceptions for the project
"""

from enums import ErrorMessage


class NotFoundException(Exception):
    """
    Exception for non-existing resource request
    """

    def __init__(self, message: str | None = None):
        """
        Args:
            message: Error Message, if None a default message would be provided
        """

        self.message = message or ErrorMessage.NOT_FOUND.value
        super().__init__(self.message)


class AlreadyExistsException(Exception):
    """
    Exception for Already Existing Resource
    """

    def __init__(self, message: str | None = None):
        """
        Args:
            message: Error Message, if None a default message would be provided
        """

        self.message = message or ErrorMessage.ALREADY_EXISTS.value
        super().__init__(self.message)
