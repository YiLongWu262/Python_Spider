# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 20:23:13 2018

@author: Administrator
"""

import Url_Manager
import Html_Downloader
import Html_Parser
import Html_Output

downloader = Html_Downloader.HtmlDownloader()
parser = Html_Parser.HtmlParser()
root_url = "https://baike.baidu.com/item/Python/407313"
html_cont = downloader.downloader(root_url)
new_urls, new_data = parser.parse(root_url,html_cont)