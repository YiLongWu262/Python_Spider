
#-*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import json
import time

import pymysql

HOST = 'localhost'
USER = 'root'
PORT = 3306

DE_DATABASE = 'temperature'
TABLE = 'chengdu'


#MySQL操作类
class MysqlClient(object):
    
    '''MySql Client'''
    def __init__(self, host=HOST,user=USER,port=PORT,db=DE_DATABASE):
        
        #连接mysql中某个数据库
        self.db = pymysql.connect(host,user,port,db,charset="utf8")#连接mysql
        self.cursor = self.db.cursor()#执行单元
        print('connect successfully')
        
    
    #创建数据库
    def createDataBase(self,name):
        sql = 'CREATE DATABASE {name} DEFAULT CHARACTER SET utf8'.format(name=name)
        try:
            self.cursor.execute(sql)
            print('create database {name} successfully'.format(name=name))
        except:
            print('create database {name} failed'.format(name=name))
    
    #在某个数据库中创建表
    def createTable(self, name):
        
        #创建数据表,下面的字段需要根据实际需求自己改
        sql = '''CREATE TABLE IF NOT EXISTS {name}(
                date date not null primary key,
                hightem int,
                lowtem int,
                temperature varchar(20),
                winddirection varchar(20),
                windpower varchar(20));'''.format(name=name)
        try:
            self.cursor.execute(sql)
            print('create table {name} successfully'.format(name=name))
        except:
            print('create table {name} failed'.format(name=name))
            
    
    #插入数据
    def insertData(self, data, table=TABLE):
        #data = {}
        #table = ''
        keys = ','.join(data.keys())
        values = ','.join(['%s']*len(data))
        sql = 'INSERT INTO {table}({keys}) VALUES ({values});'.format(table=table, keys=keys, values=values)
        try:
            if self.cursor.execute(sql, tuple(data.values())):
                print('Successful insert')
                self.db.commit()
        except:
            print('insert failed')
            self.db.rollback()
        #self.db.close()
    
    #更新数据
    def updateData(self, data, table):
        #data = {}
        #table = ''
        keys = ','.join(data.keys())
        values = ','.join(['%s']*len(data))
        sql = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=table, keys=keys, values=values)
        update = ','.join(["{key} = %s".format(key=key) for key in data])
        sql = sql + update
        try:
            if self.cursor.execute(sql, tuple(data.values())*2):
                print('Successful update')
                self.db.commit()
        except:
            print('update failed')
            self.db.rollback()
        self.db.close()
        
    def deleteData(self, table, condition):
        #table = ''
        #condition = ''
        sql = 'DELETE FROM {table} WHERE {condition}'.format(table=table, condition=condition)
        try:
            self.cursor.execute(sql)
            print('delete data successfully')
            self.db.commit()
        except:
            self.db.rollback()
        self.db.rollback()
        
    def queryData(self, condition):
        pass
    

    
#历史天气爬虫
class TianQiSpder(object):
    '''Tian qi Spider'''
    
    def __init__(self):
        self.BASE_URL = 'http://lishi.tianqi.com/'
        self.CITY = 'chengdu'#城市
        self.urls = []#存储某个城市的所有urls
        #self.datas = []#存储某个城市的所有数据
        self.countURL = 0
        self.DB = MysqlClient()#创建mysql数据库连接
        
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        }
        
    def getPage(self,url):
        try:
            response = requests.get(url, headers = self.headers)
            print(response.status_code)
            return response.text
        except:
            print('Error')
            return None
    
    def getURls(self, text):
        if text is not None:
            soup = BeautifulSoup(text, "lxml")
            tq = soup.find(class_="tqtongji1")
            for data in tq.find_all('a'):
                time = data.text#time
                year = time[0:4]#year
                month = time[5:7]#month
                time = year + month#time
                tq_url = data.get('href')#url
                #print('time:{time} url:{tq_url}'.format(time = time, tq_url = tq_url))
                self.urls.append({'time':time,'tq_url':tq_url})
            self.countURL = len(self.urls)
            
    def crawl(self):
        if self.empty():
            return
        else:
            urldata = self.urls.pop()
            time = urldata['time']
            link = urldata['tq_url']
            self.countURL = self.countURL - 1
            print(self.countURL)
            print(link)
            r = self.getPage(link)
            if r is not None:
                soup1 = BeautifulSoup(r, "lxml")
                tqtongji = soup1.find(class_="tqtongji2")
                monthData = self.getMonthData(tqtongji)
                
                #保存数据到MYsql
                self.saveData2MySQL(monthData)
                #self.datas.append(monthData)
            else:
                print('Error')
            
    #获取每个月的数据
    def getMonthData(self,tqtongji):
        month_datas = []
        
        for item in tqtongji.find_all('ul'):
            if item.get('class') is None:
                childern = item.findChildren()
                date = childern[0].text
                hightem = childern[1].text
                lowtem = childern[2].text
                temperature = childern[3].text
                winddirection = childern[4].text
                windpower = childern[5].text
                month_datas.append({'date':date,'hightem':hightem,'lowtem':lowtem,
                                    'temperature':temperature,'winddirection':winddirection,'windpower':windpower})
        return month_datas
    
    def empty(self):
        return len(self.urls) == 0
    
    def saveData2MySQL(self,datas):
        for item in datas:
            print(item)
            self.DB.insertData(item)
        
        
def main():
    app = TianQiSpder()
    rooturl = app.BASE_URL + app.CITY + '/index.html'
    print(rooturl)
    text = app.getPage(rooturl)
    app.getURls(text)
    #print(app.urls)
    while True:
        if app.empty():
            break
        else:
            app.crawl()
            time.sleep(10)

    app.DB.db.close()
    
    print('Successfully crawl temperature data about chengdu')
    
main()