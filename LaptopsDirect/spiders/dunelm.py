# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
import logging

class DunelmSpider(SitemapSpider):
    name = 'dunelm'
    allowed_domains = ['dunelm.com']
    sitemap_urls = ['https://www.dunelm.com/sitemap/product-sitemap.xml']
    
    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        l.add_xpath('price', '//h2[@data-testid="product-price"]/text()')
        #l.add_xpath('product_title', '//*[@id="product"]/div[2]/header/div/h1')
        #l.add_xpath('image_srcx', '//*[@id="amplienceContent"]/div/div[1]/ul/li[1]/div[2]/div/div/img/@src')
        #l.add_xpath('description', '//*[@id="product"]/div[2]/div[5]/div[1]/div[1]')
        l.add_xpath('stock', '//*[@id="quantity"]/@max')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()
