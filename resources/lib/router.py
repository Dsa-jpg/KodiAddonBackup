import uuid
from .actions import handle_search, handle_most_watched, select_streams, top_films, trending_shows, show_seasons, show_episodes, play_episode
import xbmcplugin
import xbmcgui


def router(action, params, traK, TRAKTLOGIN, webC, my_addon, addon_handle):
    # Definice směrování jako slovník, kde klíče jsou akce a hodnoty jsou funkce
    actions = {
        'search': lambda: handle_search(webC, my_addon),
        'most_watched': lambda: handle_most_watched(webC, addon_handle, my_addon),
        'select_stream': lambda: select_streams(params),
        'topfilms': lambda: top_films(traK, TRAKTLOGIN.CLIENTID, webC, my_addon, addon_handle),
        'trendingshows': lambda: trending_shows(traK, TRAKTLOGIN.CLIENTID, webC, my_addon, addon_handle),
        'list_seasons': lambda: show_seasons(traK, TRAKTLOGIN.CLIENTID, params.get('show_id'), addon_handle),
        'list_episodes': lambda: show_episodes(traK, TRAKTLOGIN.CLIENTID, params.get('show_id'), int(params.get('season')), addon_handle),
        'play_episode': lambda: play_episode(params.get('url')),
    }

    # Pokud akce existuje v našem slovníku, zavoláme ji
    if action in actions:
        actions[action]()
    else:
        # Výchozí obsah, pokud akce není známa
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

        # Přidání položky "Top 50 films"
        topfilms_url = f'plugin://plugin.video.helloworld/?action=topfilms'
        topfilms_li = xbmcgui.ListItem('Top Films')
        topfilms_li.setInfo('video', {'title': 'Top 50 films all time'})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=topfilms_url, listitem=topfilms_li, isFolder=True)

        # Přidání položky "Trending shows"
        trendingshows_url = f'plugin://plugin.video.helloworld/?action=trendingshows'
        trendingshows_li = xbmcgui.ListItem('Trending shows')
        trendingshows_li.setInfo('video', {'title': 'Top 50 Trending shows'})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=trendingshows_url, listitem=trendingshows_li, isFolder=True)

        xbmcplugin.endOfDirectory(addon_handle)