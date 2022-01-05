# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem


class AppliancesdeliveredSpider(SitemapSpider):
    name = 'appliancesdelivered'
    allowed_domains = ['appliancesdelivered.ie']
    sitemap_urls = ['https://www.appliancesdelivered.ie/robots.txt']

    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        l.add_xpath('sku', '//meta[@property="product:retailer_item_id"]/@content')
        l.add_xpath('europrice', '//meta[@property="product:price:amount"]/@content')
        l.add_xpath('stock', '//meta[@property="product:availability"]/@content')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()