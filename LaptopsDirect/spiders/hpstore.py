# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
import logging

class HPStoreSpider(SitemapSpider):
    name = 'HP-Store'
    allowed_domains = ['hp.com']
    sitemap_urls = ['https://www8.hp.com/sitemap-product-catalog.xml']
    
    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        l.add_xpath('sku', '//meta[@property="gis:product-id"]/@content')
        l.add_xpath('sku', '//meta[@itemprop="sku"]/@content')
        l.add_xpath('sku', '//p[@class="prod-nr"]/text()', re=r"^(?:[^\s]*\s){2}([^\s]*)")
        l.add_xpath('price','//meta[@property="price"]/@content')
        l.add_xpath('price', '//meta[@property="gis:product-price"]/@content')
        l.add_xpath('price','//div[@class="prod"]//p[@class="pb-price__now pb-price__now--pdp"]/nobr/text()')
        #l.add_xpath('product_title', '//*[@id="main-content"]/div/div[2]/div[1]/h1/text()')
        #l.add_xpath('image_srcx', '//div[@class="image-gallery__hero"]/a/img/@src')
        #l.add_xpath('description', '//div[@class="product-description product-description--collapsible"]')
        l.add_xpath('stock', '//div[@class="pb-delivery"]//text()')

        #Monitored Attribute on this scrape?
        #l.add_xpath('slotsqty', '//*[@id="technical-specification"]/table/tbody/tr/td[starts-with(.,"Slots Qty")]/following::td[1]/text()')
        #l.add_xpath('emptyslots', '//*[@id="technical-specification"]/table/tbody/tr/td[starts-with(.,"Empty Slots")]/following::td[1]/text()')
        #l.add_xpath('imagebrightness', '//*[@id="technical-specification"]/table/tbody/tr/td[starts-with(.,"Image Brightness")]/following::td[1]/text()')
                  
        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()