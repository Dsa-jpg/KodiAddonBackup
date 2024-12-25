import time
import sys
import urllib.parse
import uuid
import xbmcgui # type: ignore
import xbmcplugin # type: ignore
import xbmcaddon # type: ignore
import xbmc # type: ignore
from resources.lib.auth import WebShareClient
from resources.lib.dialog_utils import dialog_handler, dialog_notify
from resources.lib.actions import handle_search, handle_most_watched, play_episode, select_streams, show_episodes, show_seasons, top_films, trending_shows
from resources.lib.trakt import TraktClient
from resources.lib.config import TRAKTLOGIN

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
traK = TraktClient(TRAKTLOGIN.CLIENTID,TRAKTLOGIN.CLIENTSECRET)

salt = webC.get_salt(my_addon.getSetting('username'))
my_addon.setSetting('salt', salt)

token = webC.login()
my_addon.setSetting('token', token)

userdata = webC.userdata(my_addon.getSetting('token'))
my_addon.setSetting('vip_remaining',userdata['vip_days'])

if ( int(my_addon.getSetting('expiretime')) - int(time.time())) < 0:
    tokens = traK.get_auth_token()
    dialog_notify('Your refresh token is', tokens[0])
    my_addon.setSetting('refreshtoken',tokens[0])
    my_addon.setSetting('expiretime', tokens[1])

# Směrování akcí
if action == 'search':
    handle_search(webC, my_addon)

elif action == 'most_watched':
    
    handle_most_watched(webC,addon_handle,my_addon)

elif action == 'select_stream':

    select_streams(params)


elif action == 'topfilms':

    top_films(traK,TRAKTLOGIN.CLIENTID,webC,my_addon,addon_handle)

elif action == 'trendingshows':

    trending_shows(traK,TRAKTLOGIN.CLIENTID,webC,my_addon,addon_handle)

elif action == 'list_seasons':
    show_id = params.get('show_id')
    show_seasons(traK, TRAKTLOGIN.CLIENTID, show_id, addon_handle)

elif action == 'list_episodes':
    show_id = params.get('show_id')
    season_number = int(params.get('season'))
    show_episodes(traK, TRAKTLOGIN.CLIENTID, show_id, season_number, addon_handle)

elif action == 'play_episode':
    url = params.get('url')
    play_episode(url)

else:
    # Výchozí obsah
    xbmcplugin.setContent(addon_handle, 'movies')

    # Přidání položky "Search"
    search_url = f'plugin://plugin.video.helloworld/?action=search'
    search_li = xbmcgui.ListItem('Search')
    search_li.setInfo('video', {'title': 'Search for movies or series'})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=search_url, listitem=search_li, isFolder=False)

    # Přidání položky "Most Watched"
    most_watched_url = f'plugin://plugin.video.helloworld/?action=most_watched'
    most_watched_li = xbmcgui.ListItem('Most Watched')
    most_watched_li.setInfo('video', {'title': 'Most watched movies'})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=most_watched_url, listitem=most_watched_li, isFolder=True)

    #  Pridani polozky "Top 50 films"
    topfilms_url = f'plugin://plugin.video.helloworld/?action=topfilms'
    topfilms_li = xbmcgui.ListItem('Top Films')
    topfilms_li.setInfo('video', {'title': 'Top 50 films all time'})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=topfilms_url, listitem=topfilms_li, isFolder=True)

    # trending shows
    topfilms_url = f'plugin://plugin.video.helloworld/?action=trendingshows'
    topfilms_li = xbmcgui.ListItem('Trending shows')
    topfilms_li.setInfo('video', {'title': 'Top 50 Trending shows'})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=topfilms_url, listitem=topfilms_li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)    