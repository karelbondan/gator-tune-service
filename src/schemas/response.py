from pydantic import BaseModel


class PlaylistQueue(BaseModel):
    id: str
    title: str
    duration: str


class Song(BaseModel):
    id: str
    url: str | None
    title: str
    queue: list[PlaylistQueue] | None
    duration: str
    playlist_title: str | None
