from enum import Enum


class StatusCodes(str, Enum):
    OK = 'OK'
    UNAUTHORIZED = 'UNAUTHORIZED'
    UNKNOWN_ERROR = 'UNKNOWN_ERROR'

    USER_NOT_FOUND = 'USER_NOT_FOUND'
