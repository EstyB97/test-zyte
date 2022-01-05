# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
import logging

class PrinterlandSpider(SitemapSpider):
    name = 'printerland'
    allowed_domains = ['printerland.co.uk']
    sitemap_urls = ['https://www.printerland.co.uk/robots.txt']
    
    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        l.add_xpath('sku', '//span[@itemprop="sku"]/text()')
        l.add_xpath('price', '//div[@class="ex-vat"]/span/text()')
        l.add_xpath('stock', '//div[@class="stock vm"]//span[@class="counter"]/text()')
        l.add_xpath('stock', '//div[@class="stock vm"]//span[@class="lowstock"]/text()')
        l.add_xpath('stock', '//div[@class="stock__pip stock__pip--normal"]/text()')
                 
        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()