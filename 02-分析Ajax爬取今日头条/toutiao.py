#-*- coding: utf-8 -*-

import requests
from urllib.parse import urlencode
import os
from hashlib import md5
import time

class jinritoutiaoSpider(object):
    '''今日头条爬虫'''
    
    def __init__(self):
        self.base_url = 'https://www.toutiao.com/search_content/?'

    
    def joinUrl(self, offset):
        params = {
            'offset':offset,
            'format':'json',
            'keyword':'街拍',
            'autoload':'true',
            'count':'20',
            'cur_tab':'1'
        }
        return self.base_url + urlencode(params)
        
    def getPage(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except:
            print('Error')
    
    def get_images(self, json):
        if json.get('data'):
            for item in json.get('data'):
                title = item.get('title')
                if title is not None:
                    images = item.get('image_list')
                    for image in images:
                        yield {
                            'title':title,
                            'image':image.get('url')
                        }
                        
    def saveImage(self, item):
        if not os.path.exists(item.get('title')):
            if item.get('title') != '街拍必备！converse/匡威 1970S经典复刻版本，实拍开箱！':
                os.mkdir(item.get('title'))
            else:
                return
        try:
            response = requests.get('http:' + item.get('image'))
            print(response.status_code)
            if response.status_code == 200:
                file_path = '{0}/{1}.{2}'.format(item.get('title'), md5(response.content).hexdigest(), 'jpg')
                if not os.path.exists(file_path):
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                else:
                    print('Already Download', file_path)
        except:
            print('Falied to save image')
            

if __name__ == "__main__":
    jinri = jinritoutiaoSpider()
    for offset in range(0, 160, 20):
        print(offset)
        print('***********************')
        url = jinri.joinUrl(offset)
        jsondata = jinri.getPage(url)
        for item in jinri.get_images(jsondata):
            print(item)
            jinri.saveImage(item)
            time.sleep(1)
