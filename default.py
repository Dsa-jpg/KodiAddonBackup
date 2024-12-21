import time
import sys
import urllib.parse
import xbmcgui # type: ignore
import xbmcplugin # type: ignore
import xbmcaddon # type: ignore
import xbmc # type: ignore
from resources.lib.auth import WebShareClient
from resources.lib.dialog_utils import dialog_handler, dialog_notify
from resources.lib.actions import handle_search
from resources.lib.trakt import TraktClient

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
traK = TraktClient('049837151418f9fcc9d37d858e3543cb174e9560ce98ac101be744cc72631a37','73231b6d2dd2ff4855d42def1fdfa89d665a4b592746f73cf8ebce1308650797')

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
    xbmcplugin.setContent(addon_handle, 'movies')

    # Seznam "most watched" filmů, každý film má více streamů
    most_watched_movies = [
        {'title': 'Avatar', 'urls': ['http://example.com/movies/avatar_720p.mp4', 'http://example.com/movies/avatar_1080p.mp4']},
        {'title': 'Titanic', 'urls': ['http://example.com/movies/titanic_720p.mp4', 'http://example.com/movies/titanic_1080p.mp4']},
        {'title': 'The Dark Knight', 'urls': ['http://example.com/movies/dark_knight_720p.mp4', 'http://example.com/movies/dark_knight_1080p.mp4']},
    ]

    for movie in most_watched_movies:
        play_url = f'plugin://plugin.video.helloworld/?{urllib.parse.urlencode({"action": "select_stream", "title": movie["title"], "urls": ",".join(movie["urls"])})}'
        list_item = xbmcgui.ListItem(movie['title'])
        list_item.setInfo('video', {'title': movie['title']})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=play_url, listitem=list_item, isFolder=False)

    xbmcplugin.endOfDirectory(addon_handle)

elif action == 'select_stream':
    movie_title = params.get('title', 'Unknown Movie')
    movie_urls = params.get('urls', '').split(',')
    
    if movie_urls:
        # Zobrazí dialog pro výběr streamu
        selected_index = xbmcgui.Dialog().select(f'Select Stream for {movie_title}', movie_urls)
        if selected_index != -1:
            selected_url = movie_urls[selected_index]
            xbmcgui.Dialog().notification('Playing', movie_title, xbmcgui.NOTIFICATION_INFO)
            xbmc.Player().play(selected_url)
        else:
            xbmcgui.Dialog().ok('Error', 'No stream selected.')
    else:
        xbmcgui.Dialog().ok('Error', 'No URLs available for this movie.')

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

    xbmcplugin.endOfDirectory(addon_handle)
