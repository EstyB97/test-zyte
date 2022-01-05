# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
import logging

class directdiscountsSpider(SitemapSpider):
    name = 'directdiscounts'
    allowed_domains = ['direct-discounts.com']
    sitemap_urls = ['https://www.direct-discounts.com/sitemap_index.xml']
    
    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        l.add_xpath('sku', '//span[@class="sku"]/text()')
        l.add_xpath('price', '//div[@class="summary entry-summary"]//span[@class="woocommerce-Price-amount amount"]/text()')
        l.add_xpath('stock', '//input[@name="quantity"]/@value')
               
        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()