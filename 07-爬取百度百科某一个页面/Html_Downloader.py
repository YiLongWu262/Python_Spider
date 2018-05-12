

from urllib import request

class HtmlDownloader(object):
    """docstring for HtmlDownloader"""
    def __init__(self):
        pass
    
    def downloader(self, url):
        if url is None:
            return None
        response = request.urlopen(url)
        if response.getcode() != 200:
            return None
        return response.read()