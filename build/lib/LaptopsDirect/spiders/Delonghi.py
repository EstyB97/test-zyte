# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
from scrapy.loader.processors import Join
import re
from scrapy.linkextractors import LinkExtractor


class DelonghiDirectSpider(SitemapSpider):
    name = 'Delonghi-Direct'
    #custom_settings = { 
        #'DOWNLOADER_MIDDLEWARES' : {
        #    'LaptopsDirect.middlewares.CustomProxyMiddleware': 350,
        #    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 400,
        #}
   # }
    #rotate_user_agent = True
    allowed_domains = ['delonghi.com']
    sitemap_urls = ['http://www.delonghi.com/googlesitemap/sitemap_index.xml']

    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '//*[@id="Head"]/title/text()')
        l.add_xpath('sku', '//reevoo-badge/@sku')
        l.add_xpath('price', '//li[@class="del-pdp__main-info__prices__current"]/text()')
        l.add_xpath('stock', '//section[@class="del-pdp__main-info__stock-sku"]/text()')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()