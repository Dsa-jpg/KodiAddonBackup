import xbmc # type: ignore


def logged_message(msg:str,level: int = xbmc.LOGDEBUG):
    """
    Custom Logging for Kodi
    """
    xbmc.log(f"[MyAddonDebugging] {msg}", level)