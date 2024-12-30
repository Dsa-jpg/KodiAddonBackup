import requests
from .config import ERROR_LVL, TMDB
from .logging import logged_message



class TMDBclient:

    def __init__(self, apikey: str):
        self.apikey = apikey
        self.session = requests.Session()
    
    def _get(self, path: str, headers:dict = None) -> str:
        try:
            response = self.session.get(TMDB.BASEURL.format(path), headers=headers or {})
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logged_message(f"Request to {path} failed: {e}", ERROR_LVL.LOGWARNING)
            raise RuntimeError(f"API request to {path} failed") from e
        
    def get_poster_path(self, movie_id: int) -> str:
        response = self._get(f'/movie/{movie_id}?api_key={self.apikey}')
        return TMDB.PICTUREURL.format(response['poster_path'])
    
    def get_overview(self, movie_id: int) -> str:
        response = self._get(f'/movie/{movie_id}?api_key={self.apikey}')
        return response['overview']
    
    def get_language(self, movie_id: int) -> str:
        response = self._get(f'/movie/{movie_id}?api_key={self.apikey}')
        return response['original_language']
    
    def get_show_poster_path(self, show_id: int) -> str:
        response = self._get(f'/tv/{show_id}?api_key={self.apikey}')
        return TMDB.PICTUREURL.format(response['poster_path'])
    
    def get_show_overview(self, show_id: int) -> str:
        response = self._get(f'/tv/{show_id}?api_key={self.apikey}')
        return response['overview']
    
    def get_show(self, show_id: int,season_number) ->str:
        response = self._get(f'/tv/{show_id}/season/{season_number}?api_key={self.apikey}')
        return response
    
    def multi_search(self, query: str) -> dict:
        response = self._get(f'/search/multi?query={query}&include_adult=false&language=en-US&page=1&api_key={self.apikey}')
        return response['results']
    
    