from __future__ import annotations

import json
import os
import re
from os import path
from typing import TYPE_CHECKING, Dict, cast

import requests
from bs4 import BeautifulSoup
from pytubefix import YouTube
from yt_dlp import YoutubeDL

import src.utils.consts as consts
from src.responses.base import InvalidVideoId
from src.schemas.response import Song
from src.type.ytdl import Result
from src.utils.strings import Regexes, Strings, Log

if TYPE_CHECKING:
    from yt_dlp import _Params


class YT:
    def __init__(self) -> None:
        self.download_path = consts.DOWNLOAD_LOC
        self.__cache_loc = path.join(consts.TEMP_LOC, "cache.json")
        self.__ytdl_config: _Params = {
            "format": "m4a/mp4/bestaudio",
            "default_search": "ytsearch",
            "verbose": consts.YT_DLP_VERBOSE,
            "extractor_args": {
                "youtubepot-bgutilhttp": {
                    "base_url": [consts.BGUTIL_URL],
                },
                "youtube": {
                    "fetch_pot": ["always"],
                    "pot_trace": ["true"],
                },
            },
            "sleep_interval": 1,
            "max_sleep_interval": 3,
            "cookiefile": path.join(consts.TEMP_LOC, "cookies.txt"),
            "nocheckcertificate": True,
            "ignore_no_formats_error": True,
        }
        self.__url_valid_check_header = {
            "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36",
            "Range": "bytes=0-1023",
        }

    def __get_cache(self, video_id: str):
        if path.isfile(self.__cache_loc):
            with open(self.__cache_loc, "r") as stored:
                cache: Dict = json.load(stored)
                try:
                    return Song(**cache[video_id])
                except KeyError:
                    return None
        return None

    def __write_cache(self, yt: Result):
        with open(self.__cache_loc, "r+") as stored:
            cache: Dict = json.loads(stored.read())
            music_cache = Song(
                id=yt["id"],
                url=yt["url"],
                title=yt["title"],
                duration=yt["duration_string"],
                queue=None,
                playlist_title=None,
            ).__dict__
            cache[yt["id"]] = music_cache
            stored.seek(0)
            stored.write(json.dumps(cache, indent=4))
            stored.truncate()

    def __youtube(self, video_id: str):
        # check cache and the url validity if exists
        cached = self.__get_cache(video_id)
        if cached and cached.url:
            url_valid = requests.get(
                url=cached.url,
                headers=self.__url_valid_check_header,
                timeout=(5, 5),
            )
            print(Log.CACHE_AVAIL.format(video_id))
            # still valid if status code in 200 range
            if url_valid.status_code // 100 == 2:  #
                return cached

        # fetches new data if cache doesn't exist and/or url has expired
        with YoutubeDL(self.__ytdl_config) as yt:
            result = cast(Result, yt.extract_info(video_id, download=False))
            if "url" not in result:
                raise InvalidVideoId()
            self.__write_cache(result)
            return Song(
                id=result["id"],
                url=result["url"],
                title=result["title"],
                queue=None,
                duration=result["duration_string"],
                playlist_title=None,
            )

    def __find_id(self, query: str):
        """Check if the given query is a youtube link, if not then return nothing"""
        try:
            # if query is a possible id then just return it
            if len(re.findall(Regexes.YT_VIDEO_ID, query)) > 0:
                return query
            else:
                return re.findall(Regexes.YT_URL, query)[0][-1]
        except IndexError:
            return None

    def __result(self, response: requests.Response):
        # parse response using bs4 and get search result
        soup = BeautifulSoup(response.content.decode("utf-8"), features="html5lib")
        # the index of the script that contains the data varies by time.
        # at the time of this writing it was 23. for loop is better to reduce
        # the script breaking from changes made by yt
        scripts = soup.find_all("script")
        for details in scripts:
            if "ytInitialData" in str(details):
                data = re.findall(Regexes.YT_INIT_DATA, str(details))
                return json.loads(data[0])

    def search(self, query: str) -> Song:
        # check if song is a yt link
        id = self.__find_id(query=query)
        if id:
            return self.__youtube(id)

        # search youtube
        response = requests.get(url=consts.URL + query, headers=consts.HEADERS)

        # get json response
        videos = self.__result(response=response)

        # actually get the list of result
        assert videos is not None
        videos = videos["contents"]["twoColumnSearchResultsRenderer"][
            "primaryContents"
        ]["sectionListRenderer"]["contents"]

        # apparently yt also includes "adSlotRenderer" in the first index so yeah
        is_adv: dict = videos[0]["itemSectionRenderer"]["contents"][0]
        if list(is_adv.keys())[0] == "adSlotRenderer":
            videos = videos[1]["itemSectionRenderer"]["contents"]
        else:
            videos = videos[0]["itemSectionRenderer"]["contents"]

        # and get the first one
        # apparently yt includes "didYouMeanRenderer" if it thinks there's a typo in the query
        # also try to search for the first valid song for 10 times, if fails then just fail
        video_id = video_title = video_duration = ""
        for idx, songs in enumerate(videos):
            assert isinstance(songs, Dict)
            if idx > 10:
                break
            try:
                first_result = songs["videoRenderer"]
                video_id: str = first_result["videoId"]
                video_title: str = first_result["title"]["runs"][0]["text"]
                video_duration: str = first_result["lengthText"]["simpleText"]
                break
            except KeyError:
                continue

        return Song(
            id=video_id,
            url=None,
            title=video_title,
            queue=None,
            duration=video_duration.replace(".", ":"),
            playlist_title=None,
        )

    def stream(self, video_id: str) -> str:
        id = self.__find_id(video_id)
        if not id:
            raise InvalidVideoId()
        yt = self.__youtube(id)
        if not yt.url:
            raise InvalidVideoId()
        return yt.url

    def url(self, video_id: str) -> str:
        """This method is mainly used to trigger the oauth prompt"""
        yt = YouTube(url=consts.YT + video_id, use_oauth=True)
        audio = yt.streams.get_audio_only()
        assert audio
        return audio.url

    def health(self) -> str:
        return Strings.HEALTH_DRAMATIC

    def remove(self, id: str):
        music_loc = "{}/{}.m4a".format(consts.DOWNLOAD_LOC, id)
        if path.isfile(music_loc):
            os.remove(music_loc)
