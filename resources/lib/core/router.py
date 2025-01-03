from .actions import handle_search, handle_most_watched, select_streams, settings, top_films, trending_shows, show_seasons, show_episodes, play_episode, change_login_credentials
import xbmcplugin
import xbmcgui
from resources.lib.model.item import DirectoryItem


def router(action, params, traK, TRAKTLOGIN, webC, my_addon, addon_handle, tmdb,sqlDB):
    # Definice směrování jako slovník, kde klíče jsou akce a hodnoty jsou funkce
    actions = {
        'search': lambda: handle_search(webC, my_addon,tmdb,addon_handle),
        'most_watched': lambda: handle_most_watched(webC, addon_handle, my_addon),
        'select_stream': lambda: select_streams(params),
        'topfilms': lambda: top_films(traK, TRAKTLOGIN.CLIENTID, webC, my_addon, addon_handle, tmdb,sqlDB),
        'trendingshows': lambda: trending_shows(traK, TRAKTLOGIN.CLIENTID, webC, my_addon, addon_handle, tmdb),
        'list_seasons': lambda: show_seasons(traK, TRAKTLOGIN.CLIENTID, params.get('show_id'), addon_handle, tmdb),
        'list_episodes': lambda: show_episodes(traK, TRAKTLOGIN.CLIENTID, params.get('show_id'), int(params.get('season')), addon_handle, my_addon, webC, tmdb),
        'play_episode': lambda: play_episode(params.get('url'),params),
        'settings': lambda: settings(my_addon,addon_handle),
        'change_login_credentials': lambda: change_login_credentials(my_addon)
    }

    # Pokud akce existuje v našem slovníku, zavoláme ji
    if action in actions:
        actions[action]()
    else:
        # Výchozí obsah, pokud akce není známa
        xbmcplugin.setContent(addon_handle, 'movies')

        # Přidání položky "Search"
        DirectoryItem('Search', 
                      f'plugin://plugin.video.helloworld/?action=search',
                      True,
                      {'title': 'Search for movies or series'},
                      {'icon': 'special://home/addons/plugin.video.helloworld/resources/icons/search.png'}).add_to_directory(addon_handle)

        # Přidání položky "Most Watched"
        DirectoryItem('Most Watched', 
                      f'plugin://plugin.video.helloworld/?action=most_watched',
                      True,
                      {'title': 'Most watched movies'}).add_to_directory(addon_handle)
        
        # Přidání položky "Top 50 films"
        DirectoryItem('Top Films', 
                      f'plugin://plugin.video.helloworld/?action=topfilms',
                      True,
                      {'title': 'Top 50 films all time'}).add_to_directory(addon_handle)
        
        # Přidání položky "Trending shows"
        DirectoryItem('Trending Shows', 
                      f'plugin://plugin.video.helloworld/?action=trendingshows',
                      True,
                      {'title': 'Trending shows'}).add_to_directory(addon_handle)
        
        # Open addon Settings
        DirectoryItem('Settings', 
                      f'plugin://plugin.video.helloworld/?action=settings',
                      True,
                      {'title': 'Settings'}).add_to_directory(addon_handle)
        

        xbmcplugin.endOfDirectory(addon_handle)
