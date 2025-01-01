import requests
from .config import ERROR_LVL, TMDB
from .logging import logged_message



class TMDBclient:
    """Class to interact with the TMDB API."""

    def __init__(self, apikey: str):
        self.apikey = apikey
        self.session = requests.Session()
    
    def _get(self, path: str, headers:dict = None) -> str:
        """Internal method to make a GET request to the TMDB API.
        Args:
            path (str): The API path to call.
            headers (dict): Additional headers to send.
        Returns:
            str: The response text.
        Raises:
            RuntimeError: If the request fails."""
        
        try:
            response = self.session.get(TMDB.BASEURL.format(path), headers=headers or {})
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logged_message(f"Request to {path} failed: {e}", ERROR_LVL.LOGWARNING)
            raise RuntimeError(f"API request to {path} failed") from e
        
    def get_poster_path(self, movie_id: int) -> str:
        """Gets the poster path for a given movie ID.
        Args:
            movie_id (int): The TMDB movie ID.
        Returns:
            str: The URL to the poster image."""
        
        response = self._get(f'/movie/{movie_id}?api_key={self.apikey}')
        return TMDB.PICTUREURL.format(response['poster_path'])
    
    def get_overview(self, movie_id: int) -> str:
        """Gets the overview for a given movie ID.
        Args:
            movie_id (int): The TMDB movie ID.
        Returns:
            str: The movie overview."""
        
        response = self._get(f'/movie/{movie_id}?api_key={self.apikey}')
        return response['overview']
    
    def get_language(self, movie_id: int) -> str:
        """Gets the original language for a given movie ID.
        Args:
            movie_id (int): The TMDB movie ID.
        Returns:
            str: The original language of the movie."""
        
        response = self._get(f'/movie/{movie_id}?api_key={self.apikey}')
        return response['original_language']
    
    def get_show_poster_path(self, show_id: int) -> str:
        """Gets the poster path for a given show ID.
        Args:
            show_id (int): The TMDB show ID.
        Returns:
            str: The URL to the poster image."""
        response = self._get(f'/tv/{show_id}?api_key={self.apikey}')
        return TMDB.PICTUREURL.format(response['poster_path'])
    
    def get_film_poster_path(self, show_id: int) -> str:
        """Gets the poster path for a given show ID.
        Args:
            show_id (int): The TMDB show ID.
        Returns:
            str: The URL to the poster image."""
        response = self._get(f'/movie/{show_id}?api_key={self.apikey}')
        return TMDB.PICTUREURL.format(response['poster_path'])
    
    def get_film_fanart_path(self, show_id: int) -> str:
        """Gets the poster path for a given show ID.
        Args:
            show_id (int): The TMDB show ID.
        Returns:
            str: The URL to the poster image."""
        response = self._get(f'/movie/{show_id}/images?api_key={self.apikey}')
        return TMDB.TRUESIZEURL.format(response['backdrops'][0]['file_path'])
    
    def get_movie_info(self, movie_id: int) -> str:
        """Gets the movie info for a given movie ID.
        Args:
            movie_id (int): The TMDB movie ID.
        Returns:
            str: The movie info."""
        
        response = self._get(f'/movie/{movie_id}?api_key={self.apikey}')
        return response
    
    def get_show_overview(self, show_id: int) -> str:
        """Gets the overview for a given show ID.
        Args:
            show_id (int): The TMDB show ID.
        Returns:
            str: The show overview."""
        
        response = self._get(f'/tv/{show_id}?api_key={self.apikey}')
        return response['overview']
    
    def get_show(self, show_id: int, season_number:int) ->str:
        """Gets the show data for a given show ID.
        Args:
            show_id (int): The TMDB show ID.
        Returns:
            str: The show data."""
        
        response = self._get(f'/tv/{show_id}/season/{season_number}?api_key={self.apikey}')
        return response
    
    def get_episode_info(self, show_id: int, season_number: int, episode_number: int) -> str:
        """Gets the episode info for a given show ID, season and episode number.
        Args:
            show_id (int): The TMDB show ID.
            season_number (int): The season number.
            episode_number (int): The episode number.
        Returns:
            str: The episode info."""
        
        response = self._get(f'/tv/{show_id}/season/{season_number}/episode/{episode_number}?api_key={self.apikey}')
        return response
    
    def multi_search(self, query: str) -> dict:
        """Searches for movies, shows and people.
        Args:
            query (str): The search query.
        Returns:
            dict: The search results."""
        response = self._get(f'/search/multi?query={query}&include_adult=false&language=en-US&page=1&api_key={self.apikey}')
        return response['results']
    
    