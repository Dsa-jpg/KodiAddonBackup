import uuid
import xbmcgui # type: ignore
from resources.lib.dialog_utils import dialog_notify

def handle_search(webC, addon):
    """Zpracování vyhledávání."""
    keyboard = xbmcgui.Dialog().input('Enter movie or series name', type=xbmcgui.INPUT_ALPHANUM)
    if keyboard:
        try:
            searchdata = webC.search(keyboard, addon.getSetting('token'),user_uuid=str(uuid.uuid4()))
            dialog_notify("Search", str(searchdata))
        except Exception as e:
            xbmcgui.Dialog().notification("Search Error", str(e), xbmcgui.NOTIFICATION_ERROR)
