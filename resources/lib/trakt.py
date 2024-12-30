from datetime import datetime
import webbrowser
from .config import URL_API, ERROR_LVL
import requests
import json
from .logging import logged_message
from .dialog_utils import dialog_handler, dialog_notify, dialog_ok
import xbmcaddon # type: ignore

my_addon = xbmcaddon.Addon()

class TraktClient():
    """Class to interact with the Trakt.tv API."""

    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret    
        self.session = requests.Session()

    def _post(self, path: str, json: dict = None, headers:dict = None) -> str:
        """Internal method to make a POST request to the Trakt.tv API.
        Args:
            path (str): The API path to call.
            json (dict): The JSON payload to send.
            headers (dict): Additional headers to send.
        Returns:
            str: The response text.
        Raises:
            RuntimeError: If the request fails."""
        try:
            response = self.session.post(URL_API.TRAKT_BASE_URL.format(path), json=json or {}, headers=headers or {})
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logged_message(f"Request to {path} failed: {e}", ERROR_LVL.LOGWARNING)
            raise RuntimeError(f"API request to {path} failed") from e
        

    def _get(self, path: str, headers:dict = None) -> str:
        """Internal method to make a GET request to the Trakt.tv API.
        Args:
            path (str): The API path to call.
            headers (dict): Additional headers to send.
        Returns:
            str: The response text.
        Raises:
            RuntimeError: If the request fails."""
        try:
            response = self.session.get(URL_API.TRAKT_BASE_URL.format(path), headers=headers or {})
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logged_message(f"Request to {path} failed: {e}", ERROR_LVL.LOGWARNING)
            raise RuntimeError(f"API request to {path} failed") from e

        
    def get_auth_token(self):
        """Gets the auth token from the user. 
        Returns:
            tuple: The refresh token and the expiration time."""
        
    
        webbrowser.open(URL_API.AUTH_TRAKT_URL.format(self.client_id,URL_API.REDIRECT_URL))
        dialog_handler('authtoken', 'Enter your authtoken ', 'Authtoken')

        response = self._post('/oauth/token',json={
                    "code": my_addon.getSetting('authtoken'),
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "redirect_uri": URL_API.REDIRECT_URL,
                    "grant_type": "authorization_code"
            })

        expires_in_sec = response["expires_in"]
        created_at = response["created_at"]
        ex = int(expires_in_sec) + int(created_at)
        ex2 = str(datetime.fromtimestamp(ex))

        
        return response["refresh_token"],str(ex)
    
    def refresh_auth_token(self, refreshtoken: str):
        """Refreshes the auth token.
        Args:
            refreshtoken (str): The refresh token to use.
        Returns:    
            tuple: The refresh token and the expiration time."""
        
        response = self._post('/oauth/token',json={
                    "code": refreshtoken,
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "redirect_uri": URL_API.REDIRECT_URL,
                    "grant_type": "refresh_token"
            })
        
        expires_in_sec = response["expires_in"]
        created_at = response["created_at"]
        ex = int(expires_in_sec) + int(created_at)

        return response["refresh_token"],str(ex)
    
    def get_popular_movies(self, apikey: str, limit: int):
        """Gets the most popular movies.
        Args:
            apikey (str): The API key to use.
            limit (int): The number of movies to return.
        Returns:
            list: The list of popular movies."""

        response = self._get(f'/movies/popular?limit={limit}', headers={
                    "Content-Type": "application/json",
                    "trakt-api-version": "2",
                    "trakt-api-key": apikey,
        })

        return response
    
    def get_show_seasons(self, show_id: str, apikey: str):
        """Gets the seasons for a show.
        Args:
            show_id (str): The show ID to use.
            apikey (str): The API key to use.
        Returns:
            list: The list of seasons."""

        response = self._get(f'/shows/{show_id}/seasons', headers={
            "Content-Type": "application/json",
            "trakt-api-version": "2",
            "trakt-api-key": apikey,
        })
        
        return response
    
    def get_trending_shows(self, apikey: str, limit: int):
        """Gets the trending shows.
        Args:
            apikey (str): The API key to use.
            limit (int): The number of shows to return.
        Returns:
            list: The list of trending shows."""

        response = self._get(f'/shows/trending?limit={limit}', headers={
            "Content-Type": "application/json",
            "trakt-api-version": "2",
            "trakt-api-key": apikey,
        })

        if response and isinstance(response, list):
            return [item['show'] for item in response]
        return []
    
    def get_episodes(self, apikey: str, show_id: str, season: int):
        """Gets the episodes for a show.
        Args:
            apikey (str): The API key to use.
            show_id (str): The show ID to use.
            season (int): The season to get.
        Returns:
            list: The list of episodes."""
        
        response = self._get(f'/shows/{show_id}/seasons/{season}', headers={
            "Content-Type": "application/json",
            "trakt-api-version": "2",
            "trakt-api-key": apikey,
        })
        return response
    
    def get_show_by_id(self, apikey: str, show_id: str):
        response = self._get(f'/shows/{show_id}', headers={
            "Content-Type": "application/json",
            "trakt-api-version": "2",
            "trakt-api-key": apikey,
        })
        return response


    def get_show_id(self, apikey: str, show_id: str):
        """Gets the show ID from Trakt.tv.
        Args:
            apikey (str): The API key to use.
            show_id (str): The show ID to get.
        Returns:
            str: The show ID."""

        response = self._get(f'/search/trakt/{show_id}', headers={
            "Content-Type": "application/json",
            "trakt-api-version": "2",
            "trakt-api-key": apikey,
        })
        return response[0]['show']['ids']['tmdb']
