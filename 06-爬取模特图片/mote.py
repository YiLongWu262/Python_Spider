
#-*- coding: utf-8 -*-

import requests
import re
from pyquery import PyQuery as pq
import os


NUMBER = 5
class LeiSi(object):
    '''爬取model图片'''
    
    def __init__(self):
        self.BASE_URL = 'http://www.lesmao.me/thread-'
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        }
        
        
    def get_page(self,url):
        try:
            response = requests.get(url, headers = self.headers)
            print(response.status_code)
            return response.text
        except:
            print('Error')
    
    #解析得到一个人所有图片链接和目录名
    def parser(self,number):
        print('正在解析第{number}位MM'.format(number=number))
        ImageLists = []#一个人的所有图片链接
        for i in range(1,6,1):
            url = self.BASE_URL + str(number)+ '-'+str(i)+'-1.html'
            #print('正在爬取:{url}'.format(url=url))
            text = self.get_page(url)
            #如果是1，则获取文件夹名字
            if i == 1:
                directoryNmae = self.getName(text)
            imageurls = self.getImageUrls(text)
            for item in imageurls:
                ImageLists.append(item)
        print('解析完成')
        return directoryNmae,ImageLists
        
    #获取model名字，作为存储图像的文件夹名字
    def getName(self,text):
        doc = pq(text)
        return doc('h1').text()
    
    #查找页面中model的图片链接
    def getImageUrls(self,text):
        reg = r'<li><img alt=".*?" src="(.*?\.jpg)"'
        pattern = re.compile(reg)
        ImageUrls = re.findall(pattern, text)
        return ImageUrls
    
    #保存图片到文件夹中
    def saveImages(self,directoryName,image_urls):
        print('开始保存:{directoryName}'.format(directoryName=directoryName))
        #如果不存在directoryName文件夹，就创建
        if os.path.exists(directoryName):
            print('已经保存过{directoryName}'.format(directoryName=directoryName))
            return 
        else:
            os.mkdir(directoryName)
            
        for url in image_urls:
            name = url.split('/')[-1]
            print('++正在保存{name}'.format(name=name))
            image = requests.get(url)
            with open(directoryName+'/'+name,'wb') as f:
                f.write(image.content)
        print('保存{directoryName}完成'.format(directoryName=directoryName))

def main():
    app = LeiSi()
    for n in range(17000,19000,1):
        dirname,ImageLists = app.parser(number=n)
        app.saveImages(directoryName=dirname,image_urls=ImageLists)
    
if __name__ == "__main__":
    main()