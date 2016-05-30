# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from proxySpider_scrapy.spiders.proxySpider import ProxySpider


class ProxyPipeline(object):
    proxyId = 1 #设置一个ID号，方便多线程验证
    def process_item(self, item, spider):
        '''

        :param item:
        :param spider:
        :return:
        '''
        if spider.name == 'proxy':#需要判断是哪个爬虫

            proxySpider = ProxySpider(spider)
            proxy = {'ip':item['ip'],'port':item['port']}
            proxy_all = {'ip':item['ip'],'port':item['port'],'proxyId':self.proxyId}
            if proxySpider.db_helper.insert(proxy,proxy_all) == True:
                 self.proxyId += 1
            return item

        else:
            return item
