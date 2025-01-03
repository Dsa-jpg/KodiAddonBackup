import xbmcgui
import xbmcplugin

class Item:

    

    pass


class DirectoryItem():
    """ Represents an item in the directory list. """
    def __init__(self, label: str, url:str, isFolder: bool, info: dict, art: dict = None):
        """ 
        Represents an item in the directory list.
        :param label: The label of the item.
        :param url: The URL of the item.
        :param isFolder: Whether the item is a folder or not.
        :param info: Information about the item.
        :param art: Artwork for the item.
        """
        self.label = label
        self.url = url
        self.isFolder = isFolder
        self.info = info
        self.art = art

    def get_list_item(self):
        """ Returns a ListItem object for the item. """
        list_item = xbmcgui.ListItem(self.label)
        list_item.setInfo('video', self.info)
        if self.art:
            list_item.setArt(self.art)
        return list_item
    
    def add_to_directory(self, handle):
        """ Adds the item to the directory list. """
        xbmcplugin.addDirectoryItem(handle=handle, url=self.url, listitem=self.get_list_item(), isFolder=self.isFolder)
        
