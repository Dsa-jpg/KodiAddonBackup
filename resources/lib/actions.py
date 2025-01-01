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
        {'title': 'Avatar','language': 'en', 'duration': 162, 'video_codec': 'h264', 'resolution': '1920x1080', 'aspect_ratio': 1.78, 'audio_codec': 'AAC', 'audio_channels': 2, 'premiere_date': '2005-03-04'},
        {'title': 'Titanic','language': 'en', 'duration': 195, 'video_codec': 'h264', 'resolution': '1920x1080', 'aspect_ratio': 1.78, 'audio_codec': 'DTS', 'audio_channels': 6, 'premiere_date': '1997-12-19'},
        {'title': 'The Dark Knight','language': 'en', 'duration': 152, 'video_codec': 'h264', 'resolution': '1920x1080', 'aspect_ratio': 1.78, 'audio_codec': 'AAC', 'audio_channels': 2, 'premiere_date': '2008-07-18'}
    ]

    for movie in most_watched_movies:
        # Získání streamů pro film
        test = webC.urls_list(movie['title'], my_addon.getSetting('token'), str(uuid.uuid4()), 2)
        play_url = f'plugin://plugin.video.helloworld/?{urllib.parse.urlencode({"action": "select_stream", "title": movie["title"], "urls": ",".join(test["urls"])})}'
        language = movie.get("language").upper()
        formatted_title = f"[COLOR blue]{language}[/COLOR] [COLOR GREY]·[/COLOR] {movie['title']}"
        # Vytvoření ListItem pro film
        list_item = xbmcgui.ListItem(formatted_title)
        
        # Přidání streamových informací
        list_item.addStreamInfo('video', {
            'codec': movie['video_codec'],
            'aspect': movie['aspect_ratio'],
            'width': 1920,  
            'height': 1080,  
            'duration': movie['duration'] * 60, 
            'premiered': movie['premiere_date']
        })
        
        list_item.addStreamInfo('audio', {
            'codec': movie['audio_codec'],
            'channels': movie['audio_channels']
        })

        # Logování pro kontrolu
        xbmc.log(f"Metadata for movie: {movie['title']}", xbmc.LOGINFO)
        xbmc.log(f"Duration: {movie['duration'] * 60}", xbmc.LOGINFO)
        xbmc.log(f"Video Codec: {movie['video_codec']}", xbmc.LOGINFO)
        xbmc.log(f"Aspect Ratio: {movie['aspect_ratio']}", xbmc.LOGINFO)
        xbmc.log(f"Audio Codec: {movie['audio_codec']}", xbmc.LOGINFO)
        xbmc.log(f"Audio Channels: {movie['audio_channels']}", xbmc.LOGINFO)
        xbmc.log(f"Premiere Date: {movie['premiere_date']}", xbmc.LOGINFO)

        # Přidání položky do seznamu
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=play_url, listitem=list_item, isFolder=False)

    xbmcplugin.endOfDirectory(addon_handle)


"""
def select_streams(params):

    movie_title = params.get('title', 'Unknown Movie')
    movie_urls = params.get('urls', '').split(',')
    
    if movie_urls:
        # Zobrazí dialog pro výběr streamu
        selected_index = xbmcgui.Dialog().select(f'Select Stream for {movie_title}', movie_urls)
        if selected_index != -1:
            selected_url = movie_urls[selected_index]
            xbmcgui.Dialog().notification('Playing', movie_title, xbmcgui.NOTIFICATION_INFO)
            xbmc.Player().play(selected_url,listitem=xbmcgui.ListItem(movie_title))
        else:
            xbmcgui.Dialog().ok('Error', 'No stream selected.')
    else:
        xbmcgui.Dialog().ok('Error', 'No URLs available for this movie.')
"""

def select_streams(params):
    movie_title = params.get('title', 'Unknown Movie')
    movie_urls = params.get('urls', '').split(',')

    if movie_urls:
        # Výchozí data o streamech
        stream_details = [
            {'resolution': '1920x1080', 'duration': '02:30:00', 'codec': 'h264'},
            {'resolution': '1280x720', 'duration': '02:00:00', 'codec': 'h265'},
            {'resolution': '640x360', 'duration': '01:30:00', 'codec': 'mpeg4'}
        ]

        # Vytvoření seznamu možností pro dialog
        stream_options = [
            f"{detail['resolution']} - {detail['duration']} - {detail['codec']}"
            for detail in stream_details
        ]

        # Zobrazení dialogu pro výběr streamu
        selected_index = xbmcgui.Dialog().select(f'Select Stream for {movie_title}', stream_options)
        if selected_index != -1:
            selected_url = movie_urls[selected_index]
            xbmcgui.Dialog().notification('Playing', movie_title, xbmcgui.NOTIFICATION_INFO)
            xbmc.Player().play(selected_url,listitem=xbmcgui.ListItem(movie_title))
        else:
            xbmcgui.Dialog().ok('Error', 'No stream selected.')
    else:
        xbmcgui.Dialog().ok('Error', 'No URLs available for this movie.')


def top_films(traK, login, webC, my_addon, addon_handle, tmdb, sqlDB):

    sqlDB.create_movie_cache_table() 
    # Získání seznamu populárních filmů (limit 50)
    test = traK.get_popular_movies(login, 25)
    

    for movie in test:
        tmdb_id = movie['ids']['tmdb']

        # Zkusíme načíst data o filmu z cache
        cached_movie = sqlDB.get_movie_from_cache(tmdb_id)

        if cached_movie:
            # Pokud je film v cache, použijeme uložená data
            title, year, overview, poster_url = cached_movie
        else:
            # Pokud není film v cache, načteme data z API
            poster_url = tmdb.get_film_poster_path(tmdb_id)
            overview = tmdb.get_overview(tmdb_id)
            title = movie['title']
            year = movie['year']

            # Uložíme film do cache
            sqlDB.add_movie_to_cache(tmdb_id, title, year, overview, poster_url)

        info = tmdb.get_movie_info(tmdb_id)
        original_language = tmdb.get_language(tmdb_id)
        formatted_title = f"[COLOR blue]{original_language.upper()}[/COLOR] [COLOR grey]·[/COLOR] {movie['title']} [COLOR grey]({movie['year']})[/COLOR]"
        fanart_url = tmdb.get_film_fanart_path(tmdb_id)
        test = webC.urls_list(movie['title'],my_addon.getSetting('token'),str(uuid.uuid4()),2)
        play_url = f'plugin://plugin.video.helloworld/?{urllib.parse.urlencode({"action": "select_stream", "title": movie["title"],"urls": ",".join(test["urls"])})}'
        list_item = xbmcgui.ListItem(formatted_title)
        list_item.setInfo('video', {'title': movie['title'], 'year': movie['year'] , 'plot': overview, 'premiered': info['release_date']})
        list_item.addStreamInfo('video', {'duration': info['runtime'] * 60})
        list_item.setArt({'thumb': poster_url, 'icon': poster_url, 'fanart': fanart_url,})

        xbmcplugin.addDirectoryItem(handle=addon_handle, url=play_url, listitem=list_item, isFolder=False)
        
    sqlDB.close()
    # Ukončení adresáře
    xbmcplugin.endOfDirectory(addon_handle)

def trending_shows(traK, login, webC, my_addon, addon_handle, tmdb):
    # Získání seznamu populárních seriálů
    trending_shows = traK.get_trending_shows(login, 25)

    for show in trending_shows:
        poster_url = tmdb.get_show_poster_path(show['ids']['tmdb'])
        overview = tmdb.get_show_overview(show['ids']['tmdb'])
        info = tmdb.get_show_info(show['ids']['tmdb'])
        geners = [genre['name'] for genre in info['genres']]
        formatted_title = f"[COLOR blue]{info['original_language'].upper()}[/COLOR] [COLOR grey]·[/COLOR] {show['title']} [COLOR grey]({show['year']})[/COLOR] [COLOR grey]{'/'.join(geners)}[/COLOR]"
        fanart_url = tmdb.get_show_fanart_path(show['ids']['tmdb'])
        
        # Generování URL pro zobrazení sezón
        play_url = f'plugin://plugin.video.helloworld/?{urllib.parse.urlencode({"action": "list_seasons", "show_id": show["ids"]["trakt"]})}'
        list_item = xbmcgui.ListItem(formatted_title)
        list_item.setInfo('video', {'title': show["title"], 'year': show["year"], 'plot': overview, 'premiered': info["last_air_date"]})
        list_item.setArt({'thumb': poster_url, 'icon': poster_url, 'fanart': fanart_url})
        #TODO: Add stream info runtime across all seasons
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=play_url, listitem=list_item, isFolder=True)

    # Ukončení adresáře
    xbmcplugin.endOfDirectory(addon_handle)


def show_seasons(traK, login, show_id, addon_handle, tmdb):
    # Získání seznamu sezón pro konkrétní seriál
    seasons = traK.get_show_seasons(show_id,login)
    xbmcplugin.setContent(addon_handle, 'seasons')
    tmdb_id = traK.get_show_id(login,show_id)

    for i,season in enumerate(seasons):
        
        season_number = season["number"]
        try:
            # Pokus o načtení detailů sezóny
            response = tmdb.get_show(tmdb_id, season_number)
        except RuntimeError as e:
            xbmc.log(f"Chyba při načítání sezóny {season_number}: {e}", level=xbmc.LOGERROR)
            continue  # Přeskočení na další iteraci
        total_runtime = sum([episode['runtime'] for episode in response['episodes'] if episode.get('runtime') is not None]) # Bugging when there are no episodes or runtime is None

        xbmc.log(f"Total runtime for season {season_number}: {total_runtime}", level=xbmc.LOGINFO)
        poster_url = TMDB.PICTUREURL.format(response['poster_path']) # TODO: Add fallback image if poster_path is None
        fanart_url = tmdb.get_show_season_image(tmdb_id, season_number)
        
        play_url = f'plugin://plugin.video.helloworld/?{urllib.parse.urlencode({"action": "list_episodes", "show_id": show_id, "season": season_number})}'
        list_item = xbmcgui.ListItem(f'Season {season_number}')
        list_item.setInfo('video', {'title': f'Season {season_number}', 'plot': response['overview']})
        list_item.setArt({'thumb': poster_url, 'fanart': fanart_url})
        list_item.addStreamInfo('video', {'duration': str(total_runtime * 60)})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=play_url, listitem=list_item, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)


def show_episodes(traK, login, show_id, season_number, addon_handle, my_addon, webC, tmdb):
    # Získání seznamu epizod pro danou sezónu
    episodes = traK.get_episodes(login, show_id, season_number)
    title = traK.get_show_by_id(login, show_id)
    xbmcplugin.setContent(addon_handle, 'episodes')
    tmdb_id = traK.get_show_id(login,show_id)

    for episode in episodes:
        # Použití metody get() pro bezpečné získání hodnoty 'overview'
        
        response = tmdb.get_episode_info(tmdb_id,season_number,episode['number'])
        poster_url = TMDB.PICTUREURL.format(response['still_path'])
        fanart_url = TMDB.TRUESIZEURL.format(response['still_path'])
        duration = response['runtime'] * 60

        query = f'{title["title"]} - Season {season_number} - Episode {episode["number"]}'
        xbmcgui.Dialog().notification(query, xbmcgui.NOTIFICATION_INFO)
        test = webC.urls_list(query,my_addon.getSetting('token'),str(uuid.uuid4()),4)

        play_url = f'plugin://plugin.video.helloworld/?{urllib.parse.urlencode({"action": "play_episode", "title": episode["title"], "url": ".".join(test["urls"]), "show_title": title["title"], "season": season_number, "episode": episode["number"]})}'
        list_item = xbmcgui.ListItem(f'{episode["number"]}. {episode["title"]}')
        list_item.setInfo('video', {'title': episode["title"], 'plot': response['overview'] , 'aired': response['air_date']})
        list_item.addStreamInfo('video', {'duration': str(duration)})
        list_item.setArt({'thumb': poster_url, 'fanart': fanart_url})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=play_url, listitem=list_item, isFolder=False)

    xbmcplugin.endOfDirectory(addon_handle)


def play_episode(url, params):
    show_title = params.get('show_title', 'Unknown Show')
    season_number = params.get('season', '0')
    episode_number = params.get('episode', '0')
    episode_title = params.get('title', 'Unknown Episode')

    # Nastavení ListItem s meta informacemi
    list_item = xbmcgui.ListItem(show_title)
    list_item.setInfo('video', {
        'title': episode_title,  # Název seriálu
        'season': int(season_number),
        'episode': int(episode_number),
        'mediatype': 'episode',
        'plot': f'Season {season_number}, Episode {episode_number}: {episode_title}'  # Sezóna, Epizoda a název epizody
    })
    list_item.setProperty('IsPlayable', 'true')

    # Notifikace a přehrávání
    xbmcgui.Dialog().notification('Playing Episode', f'{show_title} - S{int(season_number):02}E{int(episode_number):02}', xbmcgui.NOTIFICATION_INFO)
    xbmc.Player().play(url, listitem=list_item)

def settings(my_addon, addon_handle):
    # Zobrazení nastavení
    my_addon.openSettings()
    xbmcplugin.endOfDirectory(addon_handle)

def change_login_credentials(my_addon):
    # Změna přihlašovacích údajů
    username: str=xbmcgui.Dialog().input('Enter your username', type=xbmcgui.INPUT_ALPHANUM)
    password: str=xbmcgui.Dialog().input('Enter your password', type=xbmcgui.INPUT_ALPHANUM)
    my_addon.setSetting('username', username)
    my_addon.setSetting('password', password)
    xbmcgui.Dialog().notification('Credentials changed', 'Your credentials have been updated', xbmcgui.NOTIFICATION_INFO)
    
    


