from typing import Annotated

from fastapi import APIRouter, Depends

import src.consts as consts
from src.utils.methods import GatorKey
from src.v1.service import YT

api_key = GatorKey(name=consts.API_KEY_NAME, auto_error=True)
router = APIRouter(
    prefix="/v1/music",
    tags=["Music"],
    dependencies=[Depends(api_key)],
)


@router.get("/")
def get_music(service: Annotated[YT, Depends(YT)], id: str):
    return service.stream(id)


@router.get("/search")
def search_and_get_music(service: Annotated[YT, Depends(YT)], query: str):
    return service.search(query)
