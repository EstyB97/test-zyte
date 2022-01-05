# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
from scrapy.loader.processors import TakeFirst


class TapwarehouseSpider(SitemapSpider):
    name = 'tapwarehouse'
    allowed_domains = ['tapwarehouse.com']
    sitemap_urls = ['https://www.tapwarehouse.com/robots.txt']

    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        l.add_xpath('sku', '//span[starts-with(.,"Product Code")]/following::td[1]/text()')
        l.add_xpath('sku', '//span[@class="code"]/text()')
        l.add_xpath('price', '//*[@id="productPrice"]/@data-base-price')
        l.add_xpath('product_title', '//*[@id="productDisplayName"]/text()')
        l.add_xpath('stock', '//strong[@data-test="stock"]/text()')
        l.add_xpath('stock', '//strong[@data-test="estimate-label-unavailable"]/text()')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()