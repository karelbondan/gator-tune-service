from typing import Optional

from fastapi import HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from starlette.requests import Request

import src.consts as consts
from src.utils.strings import Strings
from src.v1.service import YT


class GatorKey(APIKeyHeader):
    def __init__(
        self,
        *,
        name: str,
        scheme_name: str | None = None,
        description: str | None = None,
        auto_error: bool = True,
    ):
        super().__init__(
            name=name,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    def check_api_key(self, api_key: Optional[str]) -> Optional[str]:
        if not api_key:
            if self.auto_error:
                raise self.make_not_authenticated_error()
            return None
        if api_key != consts.API_KEY:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=Strings.FOUR_O_ONE,
            )
        return api_key

    async def __call__(self, request: Request) -> Optional[str]:
        api_key = request.headers.get(self.model.name)
        return self.check_api_key(api_key)


def init():
    yt = YT()
    yt.url("dQw4w9WgXcQ")
