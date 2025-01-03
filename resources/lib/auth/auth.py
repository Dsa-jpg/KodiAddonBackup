import datetime
import re
import xml.etree.ElementTree as ET
from resources.lib.core.config import URL_API, ERROR_LVL
import requests
import hashlib
from passlib.hash import md5_crypt
from resources.lib.core.logging import logged_message


class WebShareClient():


    def __init__(self, username:str, password:str):
        self.username = username
        self.password = password
        self.session = requests.Session()
    
    def _post(self,
              path: str,
              data: dict = None) -> str:
        """Internal method to make a POST request to the WebShare API."""
        try:
            response = self.session.post(URL_API.BASE_URL.format(path), data=data or {})
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logged_message(f"Request to {path} failed: {e}", ERROR_LVL.LOGWARNING)
            raise RuntimeError(f"API request to {path} failed") from e
    
    def get_salt(self,
                 username: str) -> str:
        """Fetches the salt value for a given username."""
        response = self._post('/salt/',data={"username_or_email":username})
        try:
            tree = ET.fromstring(response)
            salt = tree.find('salt').text
            return salt
        except (ET.ParseError, AttributeError):
            logged_message("Failed to parse salt from response", ERROR_LVL.LOGWARNING)
            raise ValueError("Invalid API response for salt")
    
    def _md5_crypt_hash(self,
                       password: str,
                       salt: str) -> str:
        """Generates an md5-crypt hash with a given salt and SHA1 digest."""
        md5_crypt_hash = md5_crypt.hash(password,salt=salt)
        sha1_digest = hashlib.sha1(md5_crypt_hash.encode()).hexdigest()
        return sha1_digest
        
    def login(self) -> str:
        """Logs in the user and returns the token."""
        salt = self.get_salt(self.username)
        hashed_password = self._md5_crypt_hash(self.password, salt)
        response = self._post("/login/", {"username_or_email": self.username,"password": hashed_password,"keep_logged_in": 1})
        try:
            tree = ET.fromstring(response)
            return tree.find('token').text
        except (ET.ParseError, AttributeError):
            logged_message("Failed to parse token from login response", ERROR_LVL.LOGWARNING)
            raise ValueError("Invalid API response for login")
    
    def userdata(self,
                 token: str):

        """Fetches user data including VIP status and days remaining."""
        response = self._post("/user_data/", {"wst": token})
        try:
            tree = ET.fromstring(response)
            return {
                "vip": tree.find('vip').text,
                "vip_days": tree.find('vip_days').text,
                "vip_until": tree.find('vip_until').text,
            }
        except (ET.ParseError, AttributeError):
            logged_message("Failed to parse user data from response", ERROR_LVL.LOGWARNING)
            raise ValueError("Invalid API response for user data")
    
    def search(self,
               query: str,
               token: str,
               user_uuid: str,
               limit: int) -> dict:
        """Searches for files and retrieves detailed information."""
        response = self._post("/search/", {
            "what": query,
            "sort": "rating",
            "limit": limit,
            "category": "video",
        })
        try:
            tree = ET.fromstring(response)
            files = []
            f_test = tree.findall('file')
            logged_message(f"Number of files found: {len(f_test)}",ERROR_LVL.LOGDEBUG)
            for file in tree.findall('file'):
                file_info = {
                    "ident": file.find('ident').text,
                    "size": f"{int(file.find('size').text) / (1024**3):.2f} GB"
                }
                # Get file download link
                file_link_response = self._post("/file_link/", {
                    "ident": file_info["ident"],
                    "password": "",
                    "download_type": "video_stream",
                    "device_uuid": user_uuid,
                    "force_https": 0,
                    "wst": token,
                })
                tree_file_link = ET.fromstring(file_link_response)
                file_info["download_link"] = tree_file_link.find('link').text
                files.append(file_info)
            return files
        except (ET.ParseError, AttributeError):
            logged_message("Failed to parse search results from response", ERROR_LVL.LOGWARNING)
            raise ValueError("Invalid API response for search")
        

    def urls_list(self,
               query: str,
               token: str,
               user_uuid: str,
               limit: int) -> dict:

        response = self._post("/search/", {
            "what": query,
            "sort": "rating",
            "limit": limit,
            "category": "video",
        })

        urls = {"urls":[]}
        root = ET.fromstring(response)
        for film in root:
            if film.find('ident') is None:
                continue
            ident = film.find('ident').text

            #TODO: Add a filter to exclude clips and trailers and films with size less than 1GB
            """ 
            name = film.find('name').text
            regex_pattern = rf"^(?!.*(?:clip|trailer)).*{re.escape(query)}.*$"
            filter = re.search(regex_pattern, name, re.IGNORECASE)
            if not filter:
                continue

            size = f"{int(film.find('size').text) / (1024**3):.2f}"
            if float(size) < 1:
                continue
            """
            
            # Get file download link
            _file_link_response = self._post("/file_link/", {
                    "ident": ident,
                    "password": "",
                    "download_type": "video_stream",
                    "device_uuid": user_uuid,
                    "force_https": 0,
                    "wst": token,
                })
            _reponse = ET.fromstring(_file_link_response)
            # some of the films are password restricted so you need to filter these out by this condition 
            if _reponse.find('link') is None:
                continue
            urls["urls"].append(_reponse.find('link').text)

        
        return urls
        


    