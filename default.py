import sys
import urllib.parse
import xbmcgui # type: ignore
import xbmcplugin # type: ignore
import xbmcaddon # type: ignore
from resources.lib.auth import WebShareClient
from resources.lib.dialog_utils import dialog_handler
from resources.lib.actions import handle_search

# Inicializace
addon_handle = int(sys.argv[1])
my_addon = xbmcaddon.Addon()
params = dict(urllib.parse.parse_qsl(sys.argv[2][1:]))
action = params.get('action')

if not my_addon.getSetting('username') or not my_addon.getSetting('password'):
    username = dialog_handler('username', 'Enter Username', 'Username')
    password = dialog_handler('password', 'Enter Password', 'Password')
    if username and password:
        my_addon.setSetting('username', username)
        my_addon.setSetting('password', password)

webC = WebShareClient(my_addon.getSetting('username'), my_addon.getSetting('password'))

salt = webC.get_salt(my_addon.getSetting('username'))
my_addon.setSetting('salt', salt)

token = webC.login()
my_addon.setSetting('token', token)

userdata = webC.userdata(my_addon.getSetting('token'))
my_addon.setSetting('vip_remaining',userdata['vip_days'])

# Směrování akcí
if action == 'search':
    handle_search(webC, my_addon)
else:
    # Výchozí obsah
    xbmcplugin.setContent(addon_handle, 'movies')

    # Přidání položky "Search"
    search_url = f'plugin://plugin.video.helloworld/?action=search'
    search_li = xbmcgui.ListItem('Search')
    search_li.setInfo('video', {'title': 'Search for movies or series'})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=search_url, listitem=search_li, isFolder=False)

    xbmcplugin.endOfDirectory(addon_handle)
