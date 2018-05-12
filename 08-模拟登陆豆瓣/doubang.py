
#-*- coding: utf-8 -*-


from os import remove
#import library
from urllib.request import urlretrieve

import requests
from bs4 import BeautifulSoup

try:
    import cookielib
except:
    import http.cookiejar as cookielib

try:
    from PIL import Image
except:
    pass


url = 'https://accounts.douban.com/login'
datas = {
    'redir':'https://www.douban.com/'
    'source':'index_nav',
    'remember':'on',
    'login':u'登录'

}
headers = {
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
   'Accept-Encoding': 'gzip, deflate, br',
   'Accept-Language': 'en-US, zh-Hans-CN; q=0.8, zh-Hans; q=0.6, en-IE; q=0.4, en; q=0.2',
   'Connection': 'Keep-Alive',
   'Host': 'www.douban.com',
   'Referer': 'https://www.baidu.com/link?url=YHGzVnXN6hhjMAbhm24nPY-4OzPzzaaiO2mWrvSKfaxU2pBeOXYTKOAtn_GZtTUX&wd=&eqid=8c98550e0003d207000000055ad00c38',
   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299'
}
session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename = 'cookies')
try:
    session.cookies.load(ignore_discard = True)
except:
    print("Cookies don not load")
    datas['form_email'] = input('please input your account:')
    datas['form_password'] = input('please input password:')


def get_captcha():
    '''
    get verify code and its ID
    '''
    r = requests.post(url, data = datas, headers = headers)
    if r.status_code == 200:

        page = r.text
        soup = BeautifulSoup(page, "html.parser")
        if soup is None:
            img_src = soup.find('img', id = "captcha_image").get('src')
            urlretrieve(img_src, 'captcha.jpg')
        else:
            print('soup is none, we can not find login verify image')
        try:
            im = Image.open('captcha.jpg')
            im.show()
            im.close()
        except:
            print("please open captcha.jpg in local directory")
        finally:
            captcha = input('please input captcha')
            remove('captcha.jpg')
    captcha_id = soup.find('input',{'type':'hidden','name':'captch-id'}).get('value')
    return captcha, captcha_id

def isLogin():
    '''
    confirm whether user is login by user information
    '''
    url = 'https://www.douban.com/accounts/'
    login_code = session.get(url, headers = headers, allow_redirects = False).status_code
    if login_code == 200:
        return True
    else:
        return False

def login():
    captcha_id, captcha = get_captcha()
    datas['captch-solution'] = captcha
    datas['captcha-id'] = captcha_id
    login_page = session.post(url, data = datas, header = headers)
    page = login_page.text
    soup = BeautifulSoup(page, "html.parser")
    result = soup.findAll('div', attrs = {'class':'title'})
    for item in result:
        print(item.find('a').get_text())
    session.cookies.save()

if __name__ == '__main__':
    if isLogin():
        print('login successfully')
    else:
        login()
