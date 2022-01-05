# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse2
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem

class TransparentSpider(SitemapSpider):
    name = 'Transparent'
    allowed_domains = ['transparent-uk.com']
    sitemap_urls = ['https://transparent-uk.com/robots.txt']

    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        l.add_xpath('sku', '//span[@class="sku"]/text()')
        l.add_xpath('price', '//p[@class="price"]//text()')
        l.add_xpath('stock', '//p[@class="ast-stock-detail"]//text()')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()