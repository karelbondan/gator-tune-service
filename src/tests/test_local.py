import requests

import src.utils.consts as consts
from src.utils.strings import Strings

HEADER = {consts.API_KEY_NAME: "abcdefg"}
HOST = "http://127.0.0.1"
PORT = 8000
ENDP = "{}:{}".format(HOST, PORT)
VERSION = "v2"


def test_health():
    res = requests.get(f"{ENDP}/health")
    assert res.json() == Strings.HEALTH


def test_unauthorized():
    res = requests.get(f"{ENDP}/{VERSION}/music/search?query=hehe")
    assert res.status_code == 401


def test_search():
    res = requests.get(
        f"{ENDP}/{VERSION}/music/search?query=never gonna give you up",
        headers=HEADER,
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
    res = requests.get(f"{ENDP}/{VERSION}/music/?id={id}", headers=HEADER)
    assert res.status_code == 200
    assert res.text
