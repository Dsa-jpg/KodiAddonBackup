import requests
from resources.lib.core.config import ERROR_LVL, TMDB
from resources.lib.core.logging import logged_message
from typing import Dict, Optional



class TMDBclient:
    """Class to interact with the TMDB API."""

    def __init__(self, apikey: str):
        self.apikey = apikey
        self.session = requests.Session()
        self.base_url = TMDB.BASEURL
        self.picture_url = TMDB.PICTUREURL
        self.fanart_url = TMDB.TRUESIZEURL
    
    def _get(self, path: str, headers:dict = None) -> str:
        """Internal method to make a GET request to the TMDB API.
        Args:
            path (str): The API path to call.
            headers (dict): Additional headers to send.
        Returns:
            str: The response text.
        Raises:
            RuntimeError: If the request fails."""
        url = self.base_url.format(path)
        try:
            response = self.session.get(url=url, headers=headers or {}, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as http_e:
            logged_message(f"HTTP error: {http_e}", ERROR_LVL.LOGWARNING)
        except requests.RequestException as req_e:
            logged_message(f"Request to {path} failed: {req_e}", ERROR_LVL.LOGWARNING)
        except ValueError as v_e:
            logged_message(f"Value error: {v_e}", ERROR_LVL.LOGWARNING)
        raise RuntimeError(f"API request to {path} failed")
    

    def get_poster_path(self, content_id: int, content_type: str="movie") ->  Optional[str]:
        """Gets the poster path for a given movie/show ID.
        Args:
            content_id (int): The TMDB movie ID.
            content_type (str): The type of content (movie or show).
        Returns:
            str: The URL to the poster image."""
        
        response = self._get(f'/{content_type}/{content_id}?api_key={self.apikey}')
        return self.picture_url.format(response.get('poster_path')) if response else None
    
    def get_overview(self, content_id: int, content_type: str="movie" ) ->  Optional[str]:
        """Gets the overview for a given movie/show ID.
        Args:
            content_id (int): The TMDB movie ID.
            content_type (str): The type of content (movie or show).
        Returns:
            str: The movie/show overview."""

        response = self._get(f'/{content_type}/{content_id}?api_key={self.apikey}')
        return response.get('overview') if response else None
    
    def get_language(self, content_id: int, content_type: str="movie" ) ->  Optional[str]:
        """Gets the language for a given movie/show ID.
        Args:
            content_id (int): The TMDB movie ID.
            content_type (str): The type of content (movie or show).
        Returns:
            str: The movie/show language."""

        response = self._get(f'/{content_type}/{content_id}?api_key={self.apikey}')
        return response.get('original_language') if response else None
    
    def get_fanart_path(self, content_id: int, content_type: str="movie" ) ->  Optional[str]:
        """Gets the fanart path for a given movie/show ID.
        Args:
            content_id (int): The TMDB movie ID.
            content_type (str): The type of content (movie or show).
        Returns:
            str: The URL to the fanart image."""

        response = self._get(f'/{content_type}/{content_id}?api_key={self.apikey}')
        if response and response.get('backdrops'):
            return self.fanart_url.format(response['backdrops'][0].get('file_path'))
        return None

    def get_show_season_image(self, show_id: int, season_number: int) -> Optional[str]:
        """Gets the image for a given show season.
        Args:
            show_id (int): The TMDB show ID.
            season_number (int): The season number.
        Returns:
            str: The URL to the image."""
        
        response = self._get(f'/tv/{show_id}/season/{season_number}/images?api_key={self.apikey}')
        if response and response.get('posters'):
            return self.fanart_url.format(response['posters'][0].get('file_path'))
        return None

    def get_movie_info(self, movie_id: int, language: str = "en-US") -> Optional[Dict]:
        """Gets detailed movie info.
        Args:
            movie_id (int): The TMDB movie ID.
            language (str): The language to use.
        Returns:
            dict: The movie info."""
        
        return self._get(f'/movie/{movie_id}?api_key={self.apikey}&language={language}')

    def get_show_info(self, show_id: int, language: str = "en-US") -> Optional[Dict]:
        """Gets detailed show info.
        Args:
            show_id (int): The TMDB show ID.
            language (str): The language to use.
        Returns:
            dict: The show info."""
        
        return self._get(f'/tv/{show_id}?api_key={self.apikey}&language={language}')
    
    def get_episode_info(self, show_id: int, season_number: int, episode_number: int, language: str = "en-US") -> Optional[Dict]:
        """Gets detailed episode info.
        Args:
            show_id (int): The TMDB show ID.
            season_number (int): The season number.
            episode_number (int): The episode number.
            language (str): The language to use.
        Returns:
            dict: The episode info."""
        
        return self._get(f'/tv/{show_id}/season/{season_number}/episode/{episode_number}?api_key={self.apikey}&language={language}')
    
    def get_season_info(self, show_id: int, season_number: int, language: str = "en-US") -> Optional[Dict]:
        """Gets detailed season info.
        Args:
            show_id (int): The TMDB show ID.
            season_number (int): The season number.
            language (str): The language to use.
        Returns:
            dict: The season info."""
        
        return self._get(f'/tv/{show_id}/season/{season_number}?api_key={self.apikey}&language={language}')

    def multi_search(self, query: str) -> Optional[Dict]:
        """Searches for movies and shows.
        Args:
            query (str): The query to search for.
        Returns:
            dict: The search results."""
        
        response = self._get(f'/search/multi?query={query}&include_adult=false&language=en-US&page=1&api_key={self.apikey}')
        return response.get('results') if response else None