class ErrorResponse:
    def __init__(self, message: str, type: str, status_code: int) -> None:
        self.message = message
        self.type = type
        self.status_code = status_code
