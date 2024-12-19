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
    
    def get_salt(self,
                 username):
        
        salt_response = s.post(URL_API.SALT_URL, data=self.data_(username_or_email=username))
        
        tree = ET.fromstring(salt_response.text)
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
        
        login_response = s.post(URL_API.LOGIN_URL,data=self.data_(username_or_email=username,password=self.md5_crypt_hash(password,self.get_salt(username)),keep_logged_in=1))
        tree_login = ET.fromstring(login_response.text)
        token = tree_login.find('token').text
        return token
    
    def userdata(self,
                 token):

        userdata = s.post(URL_API.USERDATA_URL, data=self.data_(wst=token))
        tree_userdata = ET.fromstring(userdata.text)
        vip = tree_userdata.find('vip').text
        vip_days = tree_userdata.find('vip_days').text
        vip_until = tree_userdata.find('vip_until').text
        return vip, vip_days, vip_until
    
    def search(self,
               search_data,
               token,
               user_uuid):
        
        search = s.post(URL_API.SEARCH_URL, data=self.data_(what=search_data, sort="rating", limit=1, category="video") )
        tree_search = ET.fromstring(search.text)
        for i in tree_search.findall('file'):
            ident = i.find('ident').text
            name = i.find('name').text
            size = i.find('size').text
            up_vote = i.find('positive_votes').text

            file_link = s.post(URL_API.FILELINK_URL,data={"ident":ident,"password": "","download_type": "video_stream","device_uuid":user_uuid,"force_https": 0,"wst": token})

            tree_filelink = ET.fromstring(file_link.text)

            download_link = tree_filelink.find('link').text

            file_info = s.post(URL_API.FILEINFO_URL,data={"wst":token,"ident":ident})

            tree_fileinfo = ET.fromstring(file_info.text)

            width = tree_fileinfo.find('width').text
            height = tree_fileinfo.find('height').text 
            length = tree_fileinfo.find('length').text
            format = tree_fileinfo.find('format').text
            file_type = tree_fileinfo.find('type').text

            return download_link, name, size, up_vote, width, height, length, format, file_type

            

    

class URL_API:
    BASE_URL = 'https://webshare.cz/api'
    SALT_URL = BASE_URL + '/salt/'
    LOGIN_URL = BASE_URL + '/login/'
    USERDATA_URL = BASE_URL + '/user_data/'
    ACCEPTTERMS_URL = BASE_URL + '/accept_terms/'
    SEARCH_URL = BASE_URL + '/search/'
    FILELINK_URL = BASE_URL + '/file_link/'
    FILEINFO_URL = BASE_URL + '/file_info/'


    