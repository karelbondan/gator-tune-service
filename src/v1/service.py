import json
import os
import re
from typing import Dict

import requests
from bs4 import BeautifulSoup
from pytubefix import YouTube

import src.consts as consts
from src.utils.strings import Strings
from src.v1.schemas.response import Song


class YT:
    def __init__(self) -> None:
        self.download_path = consts.DOWNLOAD_LOC

    def __youtube(self, video_id: str):
        yt = YouTube(url=consts.YT + video_id, use_oauth=True)

        # download the song, skip if already downloaded before
        if not os.path.isfile("{}/{}.m4a".format(self.download_path, yt.video_id)):
            audio = yt.streams.get_audio_only()
            assert audio
            audio.download(
                filename="{}.m4a".format(video_id),
                output_path=self.download_path,
            )

        return yt

    def __find_link(self, query: str):
        """Check if the given query is a youtube link, if not then return nothing"""
        yt_url_regex = (
            r"(https?:\/\/([\w\.]{1,256})?youtu(\.)?be(\.com)?/(watch\?v=)?)([\w-]+)"
        )
        try:
            video_id = re.findall(yt_url_regex, query)[0][-1]
            return self.__youtube(video_id=video_id)
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
                data = re.findall(
                    r"(?<=var ytInitialData = ).+(?=;</script>)",
                    str(details),
                )
                return json.loads(data[0])

    def search(self, query: str) -> Song:
        # check if song is a yt link
        yt = self.__find_link(query=query)

        if yt:
            return Song(
                id=yt.video_id,
                url="",
                title=yt.title,
                queue=None,
                duration=".".join(map(str, divmod(yt.length, 60))),
                playlist_title=None,
            )

        # search youtube
        response = requests.get(url=consts.URL + query, headers=consts.HEADERS)

        # get json response
        videos = self.__result(response=response)

        # actually get the list of result
        # fmt:off
        assert videos is not None
        videos = videos["contents"] \
            ["twoColumnSearchResultsRenderer"] \
            ["primaryContents"] \
            ["sectionListRenderer"]["contents"]
        # fmt:on

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
            duration=video_duration,
            playlist_title=None,
        )

    def stream(self, video_id: str) -> str:
        yt = self.__youtube(video_id=video_id)
        return "{}/music/{}".format(consts.SERVICE_URL, yt.video_id)

    def url(self, video_id: str) -> str:
        """This method is mainly used to trigger the oauth prompt"""
        yt = YouTube(url=consts.YT + video_id, use_oauth=True)
        audio = yt.streams.get_audio_only()
        assert audio
        return audio.url

    def health(self) -> str:
        return Strings.HEALTH_DRAMATIC

    def remove(self, id: str):
        path = "{}/{}.m4a".format(consts.DOWNLOAD_LOC, id)
        if os.path.isfile(path):
            os.remove(path)
