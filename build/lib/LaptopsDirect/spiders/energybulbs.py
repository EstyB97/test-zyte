# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
from scrapy.loader.processors import TakeFirst


class EnergybulbsSpider(SitemapSpider):
    name = 'energybulbs'
    allowed_domains = ['energybulbs.co.uk']
    sitemap_urls = ['https://www.energybulbs.co.uk/robots.txt']
    
    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)
        #l.default_output_processor = TakeFirst()

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        l.add_xpath('sku', '//span[@data-variant-sku]/text()')
        l.add_xpath('price', '//span[@data-product-price]/text()')
        l.add_xpath('stock', '//*[@id="Quantity"]/@value')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()