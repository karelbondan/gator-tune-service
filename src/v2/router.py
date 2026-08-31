from typing import Annotated

from fastapi import APIRouter, Depends

from src.utils import consts
from src.utils.methods import GatorKey
from src.v2.service import YT

api_key = GatorKey(name=consts.API_KEY_NAME, auto_error=True)
router = APIRouter(
    prefix="/v2/music",
    tags=["Music"],
    dependencies=[Depends(api_key)],
)


@router.get("/")
def get_music(service: Annotated[YT, Depends(YT)], id: str):
    return service.stream(id)


@router.get("/info/")
def get_music_info(service: Annotated[YT, Depends(YT)], id_or_url: str):
    """Get music info by its id or full url"""
    return service.info(id_or_url)


@router.get("/search")
def search_and_get_music(service: Annotated[YT, Depends(YT)], query: str):
    return service.search(query)


@router.get("/batch")
def search_and_get_multiple_music(service: Annotated[YT, Depends(YT)], query: str):
    return service.batch(query)
