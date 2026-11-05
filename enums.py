"""
Enums for the project
"""

from enum import Enum


class ErrorMessage(str, Enum):
    """
    Enum for Error Messages
    """

    FILE_NOT_FOUND = "File Not Found."
