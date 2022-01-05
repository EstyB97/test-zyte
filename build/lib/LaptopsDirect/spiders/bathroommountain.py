# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class BathroomMountainSpider(CrawlSpider):
    name = 'bathroommountain'
    allowed_domains = ['bathroommountain.co.uk']
    start_urls = ['https://bathroommountain.co.uk/']

    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//div[@id="viewport"]',)), 
        callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        l.add_xpath('sku', '//div[@itemprop="sku"]/text()')
        l.add_xpath('price', '//meta[@itemprop="price"]/@content')
        l.add_xpath('price', '//div[@itemprop="price"]/@content')
        l.add_xpath('stock', '//div[@class="stock-main"]/span/text()')
        l.add_xpath('stock', '//div[@itemprop="availability"]/@content')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()