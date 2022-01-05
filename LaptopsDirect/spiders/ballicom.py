# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
from scrapy.loader.processors import TakeFirst


class BallicomSpider(SitemapSpider):
    name = 'ballicom'
    custom_settings = { 
        'AUTOTHROTTLE_TARGET_CONCURRENCY': '20', 
        'CLOSESPIDER_ERRORCOUNT': '500',
        'CONCURRENT_REQUESTS': '20'  
   }
    allowed_domains = ['ballicom.co.uk']
    sitemap_urls = ['https://www.ballicom.co.uk/sitemap.xml']

    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        l.add_xpath('sku', '//div[@class="cst-prd-id"]/ul/li/span[starts-with(.,"MPN")]/following::span[1]/text()')
        #l.add_xpath('sku', '//*[@id="fmAdd2Cart"]//@data-flix-mpn')
        l.add_xpath('price', '//span[@itemprop="price"]/@content')
        l.add_xpath('stock', '//span[@class="green-stick"]/text()')
        l.add_xpath('stock', '//div[@class="out-of-stock"]/@class')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()