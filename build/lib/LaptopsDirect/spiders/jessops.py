# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider, Rule
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
import logging
from scrapy.linkextractors import LinkExtractor

class JessopsSpider(SitemapSpider):
    name = 'Jessops'
    allowed_domains = ['jessops.com']
    sitemap_urls = ['https://www.jessops.com/sitemap.xml']

    rules = (Rule(LinkExtractor(allow_domains=['jessops.com/p/']), callback='parse', follow= True),)
    
    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        l.add_xpath('sku', '/html/body/main/section[1]/div[1]/div[2]/p/span/text()')
        l.add_xpath('price', '/html/body/main/section[1]/div[1]/div[2]/div[1]/div[1]/p[1]/text()')
        l.add_xpath('product_title', '/html/body/main/section[1]/div[1]/div[2]/h1/span/text()')
        l.add_xpath('stock', '/html/body/main/section[1]/div[1]/div[2]/div[1]/div[2]/div/p[2]/text()')
            
        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()