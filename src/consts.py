import os
from typing import cast

from dotenv import load_dotenv

load_dotenv(override=True)

# app config
API_KEY = cast(str, os.getenv("API_KEY"))
SERVICE_URL = cast(str, os.getenv("SERVICE_URL"))
API_KEY_NAME = "X-API-Key"
DOWNLOAD_LOC = cast(str, os.getenv("DOWNLOAD_LOC")) or "./downloads"

# cors settings 
ALLOW_ORIGINS = cast(str, os.getenv("ALLOW_ORIGINS"))
ALLOW_METHODS = cast(str, os.getenv("ALLOW_METHODS"))

# app settings
PORT=int(cast(str, os.getenv("PORT")))
HOST=cast(str, os.getenv("HOST"))

# youtube stuff
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
}
URL = "https://www.youtube.com/results?search_query="
YT = "https://youtu.be/"
PLAYLIST = "https://www.youtube.com/playlist?list="
