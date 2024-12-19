import xml.etree.ElementTree as ET
import xbmcaddon # type: ignore
import requests
import xbmc # type: ignore
import hashlib
from passlib.hash import md5_crypt


ADDON = xbmcaddon.Addon()
USERNAME = ADDON.getSetting('username')
PASSWORD = ADDON.getSetting('password')
s = requests.Session()


class WebShareClient():


    def __init__(self):
        self.username = USERNAME
        self.password = PASSWORD
        pass

    @staticmethod
    def data_(**kwargs):

        data = {}
        for k, v in kwargs.items():
            data[k] = v
        return data
    
    def _post(self, path, data=None):

        if data is None:
            data = {}
        response = s.post(URL_API.BASE_URL2.format(path),data=data)
        return response.text
    
    def get_salt(self,
                 username):
        
        response = self._post('/salt/',data=self.data_(username_or_email=username))
        tree = ET.fromstring(response)
        salt= tree.find('salt').text
        return salt
    
    def md5_crypt_hash(self,
                       password,
                       salt):
        
        md5_crypt_hash = md5_crypt.hash(password,salt=salt)
        sha1_digest = hashlib.sha1(md5_crypt_hash.encode()).hexdigest()
        return sha1_digest
        
    def login(self,
              username,
              password):
        
        login_response = self._post('/login/',data=self.data_(username_or_email=username,password=self.md5_crypt_hash(password,self.get_salt(username)),keep_logged_in=1))
        tree_login = ET.fromstring(login_response.text)
        token = tree_login.find('token').text
        return token
    
    def userdata(self,
                 token):

        userdata = self._post('/user_data/', data=self.data_(wst=token))
        tree_userdata = ET.fromstring(userdata.text)
        vip = tree_userdata.find('vip').text
        vip_days = tree_userdata.find('vip_days').text
        vip_until = tree_userdata.find('vip_until').text
        return vip, vip_days, vip_until
    
    def search(self,
               search_data,
               token,
               user_uuid):
        
        search = self._post('/search/', data=self.data_(what=search_data, sort="rating", limit=1, category="video") )
        tree_search = ET.fromstring(search.text)
        for i in tree_search.findall('file'):
            ident = i.find('ident').text
            name = i.find('name').text
            size = i.find('size').text
            up_vote = i.find('positive_votes').text

            file_link = self._post('/file_link/',data={"ident":ident,"password": "","download_type": "video_stream","device_uuid":user_uuid,"force_https": 0,"wst": token})

            tree_filelink = ET.fromstring(file_link.text)

            download_link = tree_filelink.find('link').text

            file_info = self._post('/file_info/',data={"wst":token,"ident":ident})

            tree_fileinfo = ET.fromstring(file_info.text)

            width = tree_fileinfo.find('width').text
            height = tree_fileinfo.find('height').text 
            length = tree_fileinfo.find('length').text
            format = tree_fileinfo.find('format').text
            file_type = tree_fileinfo.find('type').text

            return name, download_link

            

    

class URL_API:
    BASE_URL = 'https://webshare.cz/api{0}'
    


    