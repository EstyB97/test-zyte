# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
import socket
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
from scrapy.loader.processors import Join
import re
from scrapy.linkextractors import LinkExtractor

class ShipItSpider(CrawlSpider):
    name = 'ShipIt'
    allowed_domains = ['shipitappliances.com']
    start_urls = ['https://www.shipitappliances.com/']

    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//ul[@class="navPages-list "]','//main[@id="product-listing-container"]')), 
        callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        #forcing new deploy version
        l.add_xpath('sku', '//dd[@itemprop="sku"]/text()')
        l.add_xpath('price', '//div[@class="froo-price-box"]//span[@class="price price--withTax"]/text()')
        l.add_xpath('stock', '//input[@id="qty[]"]/@value')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()