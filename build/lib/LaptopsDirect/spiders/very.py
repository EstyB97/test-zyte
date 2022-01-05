# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
import socket
import scrapy
import re
from scrapy import selector
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
import logging
from scrapy.loader.processors import TakeFirst
from scrapy import Request

class VerySpider(SitemapSpider):
    name = 'very'
    custom_settings = { 
        'DOWNLOADER_MIDDLEWARES' : {
            'LaptopsDirect.middlewares.CustomProxyMiddleware': 350,
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 400,
        }
    }
    allowed_domains = ['very.co.uk']
    sitemap_urls = ['https://www.very.co.uk/robots.txt']

    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        l.add_xpath('sku', '//*[@id="productMPN"]/text()')
        #l.add_xpath('ean', '//*[@id="productEAN"]/text()')
        l.add_xpath('price', '/html/head/meta[@property="product:price:amount"]/@content')
        #l.add_xpath('product_title', '//*[@id="productName"]/h1/span/text()')
        l.add_xpath('stock', '//*[@id="addToBasketButton"]/@value')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()