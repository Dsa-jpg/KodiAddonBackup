import xbmc # type: ignore

class URL_API:

    BASE_URL = 'https://webshare.cz/api{0}'


class ERROR_LVL:

    LOGDEBUG = xbmc.LOGDEBUG
    LOGINFO = xbmc.LOGINFO
    LOGWARNING = xbmc.LOGWARNING
    LOGEERROR = xbmc.LOGERROR
    LOGFATAL = xbmc.LOGFATAL