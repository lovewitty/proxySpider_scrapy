#coding:utf-8
import scrapy
from proxySpider_scrapy.db.db_helper import DB_Helper
from proxySpider_scrapy.detect.detect_proxy import Detect_Proxy
from proxySpider_scrapy.detect.detect_manager import Detect_Manager
from proxySpider_scrapy.items import ProxyItem


'''
这个类的作用是将代理数据进行爬取
'''
class ProxySpider(scrapy.Spider):
    name = 'proxy'
    start_urls = ["http://www.xicidaili.com/nn/"]
    allowed_domains = []
    db_helper = DB_Helper()
    detecter = Detect_Manager(5)
    Page_Start = 1
    Page_End = 4
    headers = {
         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en',
        'Referer':'http://www.xicidaili.com/'
    }

    def parse(self, response):
        '''
        解析出其中的ip和端口
        :param response:
        :return:
        '''

        trs = response.xpath('//tr[@class="odd" or @class=""]')
        for tr in trs:
            item = ProxyItem()
            tds = tr.xpath('./td/text()').extract()
            for td in tds:
                content = td.strip()
                if len(content)>0:
                    if content.isdigit():
                        item['port'] = content
                        print 'ip:',item['ip']
                        print 'port:',item['port']
                        break
                    if content.find('.')!= -1:
                        item['ip'] = content


            yield item
        if self.Page_Start < self.Page_End:
            new_url = self.start_urls[0]+str(self.Page_Start)
            self.Page_Start += 1
            yield scrapy.Request(new_url,headers=self.headers,callback=self.parse)

