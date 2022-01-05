# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import CrawlSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
import logging

class Footlocker(CrawlSpider):
    name = 'Footlocker'
    custom_settings = { 
        'DOWNLOADER_MIDDLEWARES' : {
            'LaptopsDirect.middlewares.CustomProxyMiddleware': 350,
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 400,
            #'LaptopsDirect.middlewares.RotatingProxyMiddleware': 610,
            #'LaptopsDirect.middlewares.BanDetectionMiddleware': 620,
        },
        'COOKIES_ENABLED' : 'False',
        'DOWNLOAD_DELAY': '8', 
        'AUTOTHROTTLE_START_DELAY': '60',
        'AUTOTHROTTLE_MAX_DELAY': '800', 
        'AUTOTHROTTLE_TARGET_CONCURRENCY': '1.0', 
        'CLOSESPIDER_ERRORCOUNT': '500',
        'CONCURRENT_REQUESTS': '1',
        'ROBOTSTXT_OBEY' : 'True',
        'CLOSESPIDER_TIMEOUT' : '345600'
    }
    allowed_domains = ['footlocker.co.uk']
    start_urls = ['https://www.footlocker.co.uk/en/product/nike-waffle-one-menshoes/314208317504.html']
    #sitemap_follow = ["^https://www.betterbathrooms.com/sitemaps/sitemap-products.*$"]
    
    def parse_item(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        #l.add_xpath('sku', '//span[@class="sku"]/text()')
        l.add_xpath('price', '//div[@class="Page-body constrained"]//span[@class="ProductPrice"]/span/text()')
        #l.add_xpath('stock', '//div[@class="StockMsg"]/span/text()')
                 
        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()