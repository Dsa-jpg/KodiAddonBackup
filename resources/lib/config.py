import xbmc # type: ignore
import datetime

class URL_API:

    BASE_URL = 'https://webshare.cz/api{0}'
    TRAKT_BASE_URL = 'https://api.trakt.tv{0}'
    IDBM_BASE_URL = 'https://api.themoviedb.org/3{0}'
    REDIRECT_URL = "urn:ietf:wg:oauth:2.0:oob"
    AUTH_TRAKT_URL = "https://trakt.tv/oauth/authorize?response_type=code&client_id={0}&redirect_uri={1}"


class ERROR_LVL:

    LOGDEBUG = xbmc.LOGDEBUG
    LOGINFO = xbmc.LOGINFO
    LOGWARNING = xbmc.LOGWARNING
    LOGEERROR = xbmc.LOGERROR
    LOGFATAL = xbmc.LOGFATAL


class TIME:

    CURRENTTIME = datetime.datetime.now()
    CURRENTTIMETOUNIX = int(datetime.datetime.timestamp(CURRENTTIME))