# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
from scrapy.loader.processors import TakeFirst


class MazumaSpider(SitemapSpider):
    name = 'Mazuma'
    allowed_domains = ['mazumamobile.com']
    sitemap_urls = ['https://www.mazumamobile.com/robots.txt']

    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        l.add_xpath('brand', '//*[@id="sell-my-mobile"]/div[3]/h1/span[1]/text()')
        l.add_xpath('model', '//*[@id="sell-my-mobile"]/div[3]/h1/span[2]/text()')
        l.add_xpath('price', '//*[@id="js-price"]/span/text()')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()