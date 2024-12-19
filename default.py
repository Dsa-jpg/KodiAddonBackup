import sys
import urllib
import xbmcgui  # type: ignore
import xbmcplugin # type: ignore
import xbmcaddon # type: ignore
from resources.lib.auth import WebShareClient
from resources.lib.dialog_utils import dialog_handler, dialog_notify
import uuid

# Inicializace addon handle a addon objektu
addon_handle = int(sys.argv[1])
my_addon = xbmcaddon.Addon()
webC = WebShareClient()
dialog2 = xbmcgui.Dialog()

if my_addon.getSetting('username') is None or my_addon.getSetting('password') is None:
    username = dialog_handler('username', 'Enter Username', 'Username')
    password = dialog_handler('password', 'Enter Password', 'Password')
else:
    pass  

salt = webC.get_salt(my_addon.getSetting('username'))
dialog_notify("Salt", salt)
my_addon.setSetting('salt', salt)

token = webC.login(my_addon.getSetting('username'),my_addon.getSetting('password'))
dialog_notify("Token",token)
my_addon.setSetting('token', token)

userdata = webC.userdata(my_addon.getSetting('token'))
dialog_notify("Userdata",userdata)
my_addon.setSetting('vip_remaining',str(userdata))

# Nastavení obsahu addon handle
xbmcplugin.setContent(addon_handle, 'movies')

# Přidání položky "Search"
search_url = f'plugin://plugin.video.helloworld/?action=search'
search_li = xbmcgui.ListItem('Search')
search_li.setInfo('video', {'title': 'Search for movies or series'})
xbmcplugin.addDirectoryItem(handle=addon_handle, url=search_url, listitem=search_li, isFolder=False)

# Ukončení adresáře
xbmcplugin.endOfDirectory(addon_handle)

# Zpracování akce "Search"
params = dict(urllib.parse.parse_qsl(sys.argv[2][1:]))
action = params.get('action')
if action == 'search':
    keyboard = xbmcgui.Dialog().input('Enter movie or series name', type=xbmcgui.INPUT_ALPHANUM)
    searchdata = webC.search(keyboard,my_addon.getSetting('token'),user_uuid=str(uuid.uuid4()))
    dialog_notify("Search",searchdata)
    
