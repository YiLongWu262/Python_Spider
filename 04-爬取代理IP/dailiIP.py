


import requests
from bs4 import BeautifulSoup
import json
import time

class AgentPool(object):
    '''IP代理池'''
    def __init__(self):
        self.MAXPAGE_SIZE = 100 #爬取的页面数量
        self.BASE_URL = 'http://www.xicidaili.com/nn/'#爬取的页面的基地址
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        }
        self.ip_lists = [] #获取到的代理池数据
        
    #获取页面
    def getPage(self,url):
        try:
            response = requests.get(url, headers = self.headers)
            print(response.status_code)
            return response.text
        except:
            print('ERROR')

    #获取数据
    def get_data(self,text):
        soup = BeautifulSoup(text, "lxml")
        tbody = soup.find('table')
        items = tbody.find_all('tr')
        for item in items:
            if len(item.find_all('td')) != 0:
                ip,port = self.getIpPort(item)#获取ip和port
                #print('ip:{ip} port:{port}'.format(ip = ip,port = port))
                tmp = {'ip':ip,'port':port}
                self.ip_lists.append(tmp)#添加到ip列表池中

    #获取ip和port
    def getIpPort(self,item):
        #确保找到ip和port，不是表头
        ip = item.find_all('td')[1].text
        port = item.find_all('td')[2].text
        return ip,port
    
    #保存ip代理池到文件
    def saveData(self):
        with open('./ip_agent.txt', 'a', encoding = 'utf-8') as f:
            for item in self.ip_lists:
                f.write(json.dumps(item, ensure_ascii = False) + '\n')

ip_agent = AgentPool()

for index in range(1,ip_agent.MAXPAGE_SIZE+1,1):
    url = ip_agent.BASE_URL + str(index)
    print(url)
    page = ip_agent.getPage(url)
    ip_agent.get_data(page)
    ip_agent.saveData()
    time.sleep(1)
    print('{index} page successfully'.format(index = index))