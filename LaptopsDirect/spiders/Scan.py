# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem

class ScanSpider(SitemapSpider):
    name = 'Scan'
    custom_settings = { 
        'DOWNLOADER_MIDDLEWARES' : {
            'LaptopsDirect.middlewares.CustomProxyMiddleware': 350,
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 400,
        },
        'USER_AGENT' : 'Squirtle Squad',
        'DOWNLOAD_DELAY': '0.08', 
        'AUTOTHROTTLE_START_DELAY': '20',
        'AUTOTHROTTLE_MAX_DELAY': '120', 
        'AUTOTHROTTLE_TARGET_CONCURRENCY': '0.4', 
        'CLOSESPIDER_ERRORCOUNT': '500',
        'CONCURRENT_REQUESTS': '1'  
   }
    allowed_domains = ['scan.co.uk']
    sitemap_urls = ['https://www.scan.co.uk/sitemap/productsxml']
    
    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        l.add_xpath('sku', '//strong[@itemprop="mpn"]/text()')
        l.add_xpath('price', '//div[@class="buyPanel"]//span[@class="price"]/text()')
        l.add_xpath('product_title', '//h1[@itemprop="name"]/text()')
        l.add_xpath('stock', '//div[@class="rightColumn"]//span/@title')
 
        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()