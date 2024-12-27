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
from resources.lib.config import TMDB, TRAKTLOGIN
from resources.lib.tmdb import TMDBclient
from resources.lib.router import router

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
tmdb = TMDBclient(TMDB.APIKEY)

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

router(action, params, traK, TRAKTLOGIN, webC, my_addon, addon_handle, tmdb)