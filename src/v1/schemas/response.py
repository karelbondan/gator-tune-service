from pydantic import BaseModel
from typing import Optional


class PlaylistQueue(BaseModel):
    id: str
    title: str
    duration: str


class Song(BaseModel):
    id: str
    url: Optional[str]
    title: str
    queue: Optional[list[PlaylistQueue]]
    duration: str
    playlist_title: Optional[str]
