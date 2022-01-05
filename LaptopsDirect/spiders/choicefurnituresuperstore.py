# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
import logging

class ChoicefurnituresuperstoreSpider(SitemapSpider):
    name = 'choicefurnituresuperstore'
    allowed_domains = ['choicefurnituresuperstore.co.uk']
    sitemap_urls = ['https://www.choicefurnituresuperstore.co.uk/robots.txt']
    
    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        l.add_xpath('price', '//span[@itemprop="price"]')
        l.add_xpath('product_title', '//*[@id="sb-site"]/form/div[3]/section/div/section/div/div/div[1]/div[2]/div[2]/div/div[1]/h1')
        l.add_xpath('stock', '//*[@id="product-get-it-by-val"]')
        l.add_xpath('sku', '//span[@itemprop="sku"]')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()