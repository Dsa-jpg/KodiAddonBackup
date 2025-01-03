import os
import time
import sys
import urllib.parse
import xbmcaddon, xbmcvfs
from resources.lib.auth.auth import WebShareClient
from resources.lib.services.trakt import TraktClient
from .config import TMDB, TRAKTLOGIN
from resources.lib.services.tmdb import TMDBclient
from resources.lib.db.db import SQlLiteDatabase
from resources.lib.utils.dialog_utils import dialog_handler

def initialize_addon():
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
    traK = TraktClient(TRAKTLOGIN.CLIENTID, TRAKTLOGIN.CLIENTSECRET)
    tmdb = TMDBclient(TMDB.APIKEY)
    profile_path = xbmcvfs.translatePath('special://profile')  

    # Cesta k databázi
    db_path = os.path.join(profile_path, 'addon_data', 'plugin.video.helloworld', 'movie_cache.db')
    sqlDB = SQlLiteDatabase(db_path)

    salt = webC.get_salt(my_addon.getSetting('username'))
    my_addon.setSetting('salt', salt)

    token = webC.login()
    my_addon.setSetting('token', token)

    userdata = webC.userdata(my_addon.getSetting('token'))
    my_addon.setSetting('vip_remaining', userdata['vip_days'])

    if (int(my_addon.getSetting('expiretime')) - int(time.time())) < 0:
        tokens = traK.get_auth_token()
        my_addon.setSetting('refreshtoken', tokens[0])
        my_addon.setSetting('expiretime', tokens[1])

    return addon_handle, my_addon, params, action, traK, TRAKTLOGIN, webC, tmdb, sqlDB
