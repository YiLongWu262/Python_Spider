#-*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time
import json

class MaoYanSpider(object):
    '''猫眼电影爬虫'''
    
    def __init__(self):
        self.base_url = 'http://maoyan.com/board/4?offset='
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        }
    
    # 获取网页
    def getPage(self, offset):
        url = self.base_url + str(offset)
        try:
            response = requests.get(url, headers = self.headers)
            if response.status_code == 200:
                return response.text
            else:
                return None
        except:
            print('Error')
            return None
    
    # 解析每个网页
    def parser(self, item):
        data = {}
        data['rank'] = item.i.get_text()
        data['title'] = item.p.a['title']
        data['poster'] = item.a.find_all('img')[1]['data-src']
        data['actors'] = item.find_all('p')[1].get_text().split()[0][3:]
        data['timeloc'] = item.find_all('p')[2].get_text().split()[0][5:]
        return data
    
    def saveData(self, data):
        with open('./maoyantop100.txt', 'a', encoding = 'utf-8') as f:
            f.write(json.dumps(data, ensure_ascii = False) + '\n')
            f.close()

    # 提取数据
    def extractData(self, page):
        if page is not None:
            soup = BeautifulSoup(page, "lxml")
            for item in soup.find_all('dd'):
                data = self.parser(item)
                print(data)
                self.saveData(data)
        else:
            print('page is none')
            


maoyan = MaoYanSpider()
for offset in range(0, 100, 10):
    print(offset)
    page = maoyan.getPage(offset)
    maoyan.extractData(page)