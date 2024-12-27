import uuid
import urllib
import xbmcgui # type: ignore
from resources.lib.dialog_utils import dialog_notify
import xbmcplugin, xbmc
from .config import TMDB

def handle_search(webC, addon, tmbd, addon_handle):
    """Handling the search"""
    keyboard = xbmcgui.Dialog().input('Enter movie or series name', type=xbmcgui.INPUT_ALPHANUM)
    if keyboard:
        try:
            # Logování zadání hledání
            xbmc.log(f"Searching for: {keyboard}", level=xbmc.LOGDEBUG)

            searchdata = tmbd.multi_search(keyboard)
            # Logování výsledků hledání
            xbmc.log(f"Search results: {str(searchdata)}", level=xbmc.LOGDEBUG)

            #dialog_notify("Search", str(searchdata))

            # Přidání položek do adresáře
            for item in searchdata:
                # Logování každé položky před přidáním do adresáře
                #xbmc.log(f"Adding item to directory: {item["name"]}", level=xbmc.LOGDEBUG)
                title = item.get("title", item.get("name", "Unknown"))
                # Vytvoří ListItem pro každou položku
                list_item = xbmcgui.ListItem(f'{title}')
                list_item.setInfo('video', {'title': title, 'plot': item["overview"]})
                list_item.setArt({'thumb': TMDB.PICTUREURL.format(item["backdrop_path"]), 'icon': TMDB.PICTUREURL.format(item["backdrop_path"])})

                # Přidání položky do adresáře
                xbmcplugin.addDirectoryItem(handle=addon_handle, url='', listitem=list_item, isFolder=False)

            # Ukončení adresáře
            xbmc.log("Ending the directory", level=xbmc.LOGDEBUG)
            xbmcplugin.endOfDirectory(addon_handle)

        except Exception as e:
            # Logování chyby
            xbmc.log(f"Search Error: {str(e)}", level=xbmc.LOGERROR)
            xbmcgui.Dialog().notification("Search Error", str(e), xbmcgui.NOTIFICATION_ERROR)

def handle_most_watched(webC, addon_handle, my_addon):
    """Handling the most watched films"""
    xbmcplugin.setContent(addon_handle, 'movies')
    # Seznam "most watched" filmů, každý film má více streamů
    most_watched_movies = [
        {'title': 'Avatar'},
        {'title': 'Titanic'},
        {'title': 'The Dark Knight'}
    ]

    for movie in most_watched_movies:
        test = webC.urls_list(movie['title'],my_addon.getSetting('token'),str(uuid.uuid4()),2)
        play_url = f'plugin://plugin.video.helloworld/?{urllib.parse.urlencode({"action": "select_stream", "title": movie["title"], "urls": ",".join(test["urls"])})}'
        list_item = xbmcgui.ListItem(movie['title'])
        list_item.setInfo('video', {'title': movie['title']})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=play_url, listitem=list_item, isFolder=False)

    xbmcplugin.endOfDirectory(addon_handle)

def select_streams(params):

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

def top_films(traK, login, webC, my_addon, addon_handle, tmdb):

    # Získání seznamu populárních filmů (limit 50)
    test = traK.get_popular_movies(login, 25)
    

    for movie in test:
        # Generování URL pouze s akcí a názvem filmu
        poster_url = tmdb.get_poster_path(movie['ids']['tmdb'])
        overview = tmdb.get_overview(movie['ids']['tmdb'])
        test = webC.urls_list(movie['title'],my_addon.getSetting('token'),str(uuid.uuid4()),2)
        play_url = f'plugin://plugin.video.helloworld/?{urllib.parse.urlencode({"action": "select_stream", "title": movie["title"],"urls": ",".join(test["urls"])})}'
        list_item = xbmcgui.ListItem(f'{movie["title"]} ({movie["year"]})')
        list_item.setInfo('video', {'title': movie['title'], 'year': movie['year'] , 'plot': overview})
        list_item.setArt({'thumb': poster_url, 'icon': poster_url, 'fanart': poster_url,})

        xbmcplugin.addDirectoryItem(handle=addon_handle, url=play_url, listitem=list_item, isFolder=False)

    # Ukončení adresáře
    xbmcplugin.endOfDirectory(addon_handle)

def trending_shows(traK, login, webC, my_addon, addon_handle, tmdb):
    # Získání seznamu populárních seriálů
    trending_shows = traK.get_trending_shows(login, 25)

    for show in trending_shows:
        poster_url = tmdb.get_show_poster_path(show['ids']['tmdb'])
        overview = tmdb.get_show_overview(show['ids']['tmdb'])
        # Generování URL pro zobrazení sezón
        play_url = f'plugin://plugin.video.helloworld/?{urllib.parse.urlencode({"action": "list_seasons", "show_id": show["ids"]["trakt"]})}'
        list_item = xbmcgui.ListItem(f'{show["title"]} ({show["year"]})')
        list_item.setInfo('video', {'title': show["title"], 'year': show["year"], 'plot': overview})
        list_item.setArt({'thumb': poster_url, 'icon': poster_url, 'fanart': poster_url})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=play_url, listitem=list_item, isFolder=True)

    # Ukončení adresáře
    xbmcplugin.endOfDirectory(addon_handle)


def show_seasons(traK, login, show_id, addon_handle, tmdb):
    # Získání seznamu sezón pro konkrétní seriál
    seasons = traK.get_show_seasons(show_id,login)
    xbmcplugin.setContent(addon_handle, 'seasons')

    for season in seasons:
        season_number = season["number"]
        play_url = f'plugin://plugin.video.helloworld/?{urllib.parse.urlencode({"action": "list_episodes", "show_id": show_id, "season": season_number})}'
        list_item = xbmcgui.ListItem(f'Season {season_number}')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=play_url, listitem=list_item, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)


def show_episodes(traK, login, show_id, season_number, addon_handle, my_addon, webC, tmdb):
    # Získání seznamu epizod pro danou sezónu
    episodes = traK.get_episodes(login, show_id, season_number)
    title = traK.get_show_by_id(login, show_id)
    xbmcplugin.setContent(addon_handle, 'episodes')

    for episode in episodes:
        # Použití metody get() pro bezpečné získání hodnoty 'overview'

        query = f'{title["title"]} - Season {season_number} - Episode {episode["number"]}'
        xbmcgui.Dialog().notification(query, xbmcgui.NOTIFICATION_INFO)
        test = webC.urls_list(query,my_addon.getSetting('token'),str(uuid.uuid4()),4)
        overview = episode.get("overview", "No overview available.")
        #dummy_url = f'https://example.com/play/{show_id}/{season_number}/{episode["number"]}'
        play_url = f'plugin://plugin.video.helloworld/?{urllib.parse.urlencode({"action": "play_episode", "url": ".".join(test["urls"])})}'
        list_item = xbmcgui.ListItem(f'{episode["number"]}. {episode["title"]}')
        list_item.setInfo('video', {'title': episode["title"], 'plot': overview})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=play_url, listitem=list_item, isFolder=False)

    xbmcplugin.endOfDirectory(addon_handle)


def play_episode(url):
    xbmcgui.Dialog().notification('Playing Episode', 'Starting playback...', xbmcgui.NOTIFICATION_INFO)
    xbmc.Player().play(url)

def settings(my_addon, addon_handle):
    # Zobrazení nastavení
    my_addon.openSettings()
    xbmcplugin.endOfDirectory(addon_handle)


