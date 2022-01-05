# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
import logging

class HeliguySpider(SitemapSpider):
    name = 'Heliguy'
    allowed_domains = ['heliguy.com']
    sitemap_urls = ['https://www.heliguy.com/robots.txt']
    
    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '//*[@id="html-products"]/head/title/text()')
        l.add_xpath('sku', '//*[@id="js-product-reference"]/text()')
        l.add_xpath('price', '//*[@id="js-product-price"]/span[1]/span/text()')
        l.add_xpath('product_title', '//*[@id="js-product-title"]/text()')
        l.add_xpath('stock', '//*[@id="js-product-total-stock"]/span')
            
        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()