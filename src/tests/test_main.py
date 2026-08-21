from fastapi.testclient import TestClient

from src.main import app
from src.utils import consts
from src.utils.strings import Strings

client = TestClient(app)
header = {consts.API_KEY_NAME: consts.API_KEY}


def test_health():
    res = client.get("/health")
    assert res.json() == Strings.HEALTH


def test_unauthorized():
    res = client.get("/v2/music/search?query=hehe")
    assert res.status_code == 401


def test_search():
    res = client.get(
        "/v2/music/search?query=never gonna give you up",
        headers=header,
    )
    assert res.json() == {
        "id": "dQw4w9WgXcQ",
        "url": None,
        "title": "Rick Astley - Never Gonna Give You Up (Official Video) (4K Remaster)",
        "queue": None,
        "duration": "3:34",
        "playlist_title": None,
    }


def test_music():
    id = "dQw4w9WgXcQ"
    res = client.get(f"/v2/music/?id={id}", headers=header)
    assert res.status_code == 200
    assert res.text
