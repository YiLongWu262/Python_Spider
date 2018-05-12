
#-*- coding: utf-8 -*-

import requests
from urllib.parse import urlencode
import re
import json

class JinDongComment(object):
    '''爬取京东的商品评论'''
    def __init__(self,page_number):
        self.BASE_URL = 'https://sclub.jd.com/comment/productPageComments.action?'
        self.params = {
            'callback':'fetchJSON comment98vv516',
            'productId':'6946635',
            'score':'0',
            'sortType':'5',
            'page':page_number,
            'pageSize':'10',
            'isShadowSku':'0',
            'rid':'0',
            'fold':'1'
        }
        self.url = self.BASE_URL + urlencode(self.params)
        
        
    def getPage(self):
        try:
            response = requests.get(self.url)
            return response.text
        except:
            print('Error')
            
    def parse(self,text):
        result = re.match('.*?\\((.*)\\);', text)
        data = json.loads(result.group(1))
        comments = data.get('comments')#获取评论
        return comments
    
    def output(self,comments):
        for item in comments:
            print(item.get('id'))
            print(item.get('content').strip())
def main():
    app = JinDongComment(page_number=5)
    text = app.getPage()
    comments = app.parse(text)
    app.output(comments)
    

if __name__ == "__main__":
    main()