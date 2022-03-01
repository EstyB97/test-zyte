# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from scrapy import Request
from LaptopsDirect.items import LaptopsdirectItem
import logging

class TherangeSpider(SitemapSpider):
    name = 'therange'
    allowed_domains = ['therange.co.uk']
    sitemap_urls = ['https://www.therange.co.uk/sitemap/sitemap-1.xml', 'https://www.therange.co.uk/sitemap/sitemap-2.xml']
    handle_httpstatus_list = [403]

    def start_requests(self):
        headers= {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
        for url in self.sitemap_urls:
            yield Request(url, headers=headers)
    
    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        l.add_xpath('price', '//*[@id="min_price"]')
        l.add_xpath('product_title', '//*[@id="product-dyn-title"]')
        l.add_xpath('description', '//*[@id="product-description"]')
        l.add_xpath('stock', '//*[@id="product-get-it-by-val"]')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()