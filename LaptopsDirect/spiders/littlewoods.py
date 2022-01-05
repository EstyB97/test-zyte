# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

#Need to improve performance

class LittlewoodsSpider(CrawlSpider):
    name = 'littlewoods'
    allowed_domains = ['littlewoods.com']
    custom_settings = { 
      'DOWNLOAD_DELAY': '0.08', 
      'AUTOTHROTTLE_START_DELAY': '2',
      'AUTOTHROTTLE_MAX_DELAY': '25', 
      'AUTOTHROTTLE_TARGET_CONCURRENCY': '16', 
      'CLOSESPIDER_ERRORCOUNT': '15000',
      'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362',
      'CONCURRENT_REQUESTS': '16', 
   }
    start_urls = ['https://www.littlewoods.com/']

    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('/html')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        l.add_xpath('sku', '//*[@id="productMPN"]/text()')
        l.add_xpath('price', '/html/head/meta[@property="product:price:amount"]/@content')
        l.add_xpath('product_title', '//*[@id="productName"]/h1/span/text()')
        l.add_xpath('stock', '//*[@id="addToBasketButton"]/@value')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()