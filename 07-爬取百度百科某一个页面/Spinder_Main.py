

import Url_Manager
import Html_Downloader
import Html_Parser
import Html_Output

class SpiderMain(object):
    """docstring for SpiderM"""
    
    def __init__(self):
        self.urls = Url_Manager.UrlManager()
        self.downloader = Html_Downloader.HtmlDownloader()
        self.parser = Html_Parser.HtmlParser()
        self.output = Html_Output.HtmlOutput()

    def craw(self, root_url):
        count = 1
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                print("crawing %d : %s" %(count,new_url))
                html_cont = self.downloader.downloader(new_url)
                new_urls, new_data = self.parser.parse(new_url,html_cont)
                self.urls.add_new_urls(new_urls)
                self.output.collect_data(new_data)
            except:
                print("craw failed")
                
            if count == 60:
                break

            count = count + 1

        self.output.output_data()

if __name__ == "__main__":
    root_url = "https://baike.baidu.com/item/Python/407313"
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)