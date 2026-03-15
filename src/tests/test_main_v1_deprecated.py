from fastapi.testclient import TestClient

import src.utils.consts as consts
from src.main import app
from src.utils.strings import Strings

client = TestClient(app)
header = {consts.API_KEY_NAME: consts.API_KEY}


def test_health():
    res = client.get("/health")
    assert res.json() == Strings.HEALTH


def test_unauthorized():
    res = client.get("/v1/music/search?query=hehe")
    assert res.status_code == 401


def test_search():
    res = client.get(
        "/v1/music/search?query=never gonna give you up",
        headers=header,
    )
    assert res.json() == {
        "id": "dQw4w9WgXcQ",
        "url": None,
        "title": "Rick Astley - Never Gonna Give You Up (Official Video) (4K Remaster)",
        "queue": None,
        "duration": "3.34",
        "playlist_title": None,
    }


def test_music():
    id = "dQw4w9WgXcQ"
    res = client.get(f"/v1/music/?id={id}", headers=header)
    assert res.json() == f"{consts.SERVICE_URL}/{id}.m4a"
