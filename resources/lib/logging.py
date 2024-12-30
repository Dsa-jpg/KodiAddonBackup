import xbmc # type: ignore
import xbmcaddon
my_addon = xbmcaddon.Addon()


def logged_message(msg:str, level: int = xbmc.LOGDEBUG):
    """
    Custom Logging for Kodi
    """
    if my_addon.getSetting('debug') == 'false':
        return None
    xbmc.log(f"[MyAddonDebugging] {msg}", level)