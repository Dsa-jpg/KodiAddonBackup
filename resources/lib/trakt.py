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

    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret    
        self.session = requests.Session()

    def _post(self, path: str, json: dict = None, headers:dict = None) -> str:
        """Internal method to make a POST request to the Trakt.tv API."""
        try:
            response = self.session.post(URL_API.TRAKT_BASE_URL.format(path), json=json or {}, headers=headers or {})
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logged_message(f"Request to {path} failed: {e}", ERROR_LVL.LOGWARNING)
            raise RuntimeError(f"API request to {path} failed") from e
        

    def _get(self, path: str, headers:dict = None) -> str:
        try:
            response = self.session.get(URL_API.TRAKT_BASE_URL.format(path), headers=headers or {})
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logged_message(f"Request to {path} failed: {e}", ERROR_LVL.LOGWARNING)
            raise RuntimeError(f"API request to {path} failed") from e

        
    def get_auth_token(self):
        
            
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

        response = self._get(f'/movies/popular?limit={limit}', headers={
                    "Content-Type": "application/json",
                    "trakt-api-version": "2",
                    "trakt-api-key": apikey,
        })

        return response
    
    def get_show_seasons(self, show_id: str, apikey: str):

        response = self._get(f'/shows/{show_id}/seasons', headers={
            "Content-Type": "application/json",
            "trakt-api-version": "2",
            "trakt-api-key": apikey,
        })
        
        return response