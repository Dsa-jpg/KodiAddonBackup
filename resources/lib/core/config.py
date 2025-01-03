import xbmc # type: ignore
import datetime

class URL_API:

    BASE_URL = 'https://webshare.cz/api{0}'
    TRAKT_BASE_URL = 'https://api.trakt.tv{0}'
    IDBM_BASE_URL = 'https://api.themoviedb.org/3{0}'
    REDIRECT_URL = "urn:ietf:wg:oauth:2.0:oob"
    AUTH_TRAKT_URL = "https://trakt.tv/oauth/authorize?response_type=code&client_id={0}&redirect_uri={1}"
    IN_DB = "special://profile/addon_data/plugin.video.helloworld/movies_cache.db"


class ERROR_LVL:

    LOGDEBUG = xbmc.LOGDEBUG
    LOGINFO = xbmc.LOGINFO
    LOGWARNING = xbmc.LOGWARNING
    LOGEERROR = xbmc.LOGERROR
    LOGFATAL = xbmc.LOGFATAL


class TIME:

    CURRENTTIME = datetime.datetime.now()
    CURRENTTIMETOUNIX = int(datetime.datetime.timestamp(CURRENTTIME))


class TRAKTLOGIN:

    CLIENTID = '049837151418f9fcc9d37d858e3543cb174e9560ce98ac101be744cc72631a37'
    CLIENTSECRET = '73231b6d2dd2ff4855d42def1fdfa89d665a4b592746f73cf8ebce1308650797'


class TMDB:

    APIKEY = 'c10422c248715bff0e3f5fd24bd7d855'
    BASEURL = 'https://api.themoviedb.org/3{0}'
    PICTUREURL = 'https://media.themoviedb.org/t/p/w300_and_h450_bestv2{0}'
    TRUESIZEURL = 'https://image.tmdb.org/t/p/original/{0}'