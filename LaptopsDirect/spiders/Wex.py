# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
import logging

class WexSpider(SitemapSpider):
    name = 'Wex'
    allowed_domains = ['wexphotovideo.com']
    sitemap_urls = ['https://www.wexphotovideo.com/robots.txt']
    
    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        l.add_xpath('sku', '//*[@id="product-tabs"]/span[2]/strong/text()')
        l.add_xpath('price', '//*[@id="main-product-price"]/span/text()')
        l.add_xpath('product_title', '//*[@id="main-product-details"]/div[1]/h1/text()')
        l.add_xpath('stock', '//*[@id="stock-indicator"]/text()')
            
        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()