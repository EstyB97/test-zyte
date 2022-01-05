# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem


class ServersplusSpider(SitemapSpider):
    name = 'ServersPlus'
    allowed_domains = ['serversplus.com']
    sitemap_urls = ['https://www.serversplus.com/robots.txt']

    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        l.add_xpath('sku', '//*[@id="prodl"]/span/p[1]/em/text()')
        l.add_xpath('price', '//*[@id="prodr"]/div/h2[1]/text()')
        l.add_xpath('product_title', '//*[@id="prodl"]/h1')
        l.add_xpath('stock', '//*[@id="prodr"]/div/div[2]/div[2]/p/text()')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()