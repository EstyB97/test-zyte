# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
import socket
from scrapy.spiders import SitemapSpider, Rule
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
from scrapy.loader.processors import TakeFirst
from scrapy.linkextractors import LinkExtractor


class Devspider3spider(SitemapSpider):
    name = 'devspider3'
    custom_settings = { 
      'DOWNLOAD_DELAY': '0.08', 
      'AUTOTHROTTLE_START_DELAY': '4',
      'AUTOTHROTTLE_MAX_DELAY': '80', 
      'AUTOTHROTTLE_TARGET_CONCURRENCY': '16', 
      'CLOSESPIDER_ERRORCOUNT': '500',
      'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362',
      'CONCURRENT_REQUESTS': '24', 
   }
    allowed_domains = ['johnlewis.com']
    sitemap_urls = ['https://www.johnlewis.com/product-1.xml', 'https://www.johnlewis.com/product-2.xml', 'https://www.johnlewis.com/product-3.xml']
    #sitemap_urls = ['https://www.johnlewis.com/robots.txt']

    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        l.add_value('sku', '//div[@data-cy="product-specification-value-Model number"]/text()')
        l.add_xpath('price', '//div[@class="standard-product-column-right"]//p[@class="price price--large"]/text()')
        l.add_xpath('stock', '//*[@id="quantity"]/@value')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()