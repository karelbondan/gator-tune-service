from fastapi import status

from src.utils.strings import Strings


class ErrorResponse(Exception):
    def __init__(self, message: str, type: str, status_code: int) -> None:
        self.message = message
        self.type = type
        self.status_code = status_code


class InvalidVideoId(ErrorResponse):
    def __init__(self) -> None:
        super().__init__(
            Strings.INVALID_ID,
            self.__class__.__name__,
            status.HTTP_404_NOT_FOUND,
        )
