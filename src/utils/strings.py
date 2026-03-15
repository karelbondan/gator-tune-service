class Strings:
    HEALTH = "System's running all fine"
    FOUR_O_ONE = "Pls do not I am nothing of importance go target something else"
    HEALTH_DRAMATIC = "Your query is my command"
    INTERNAL_ERROR = "An internal error occured: {}"
    INVALID_ID = "No streamable url found with the specified video id"


class Regexes:
    YT_URL = r"(https?:\/\/([\w\.]{1,256})?youtu(\.)?be(\.com)?/(watch\?v=)?)([\w-]+)"
    YT_INIT_DATA = r"(?<=var ytInitialData = ).+(?=;</script>)"
    YT_VIDEO_ID = r"[a-zA-Z0-9_-]{11}"


class Log:
    PREFIX = "[gator]"
    CACHE_AVAIL = PREFIX + " Valid cache found for {}, using it instead of a new request"
