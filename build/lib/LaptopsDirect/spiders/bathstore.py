# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem


class BathstoreSpider(SitemapSpider):
    name = 'bathstore'
    allowed_domains = ['bathstore.com']
    sitemap_urls = ['https://www.bathstore.com/sitemap/store-sitemap.xml']

    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '//html/head/title/text()')
        l.add_xpath('sku', '//div[@id="specifications"]//td[starts-with(.,"Product SKU")]/following::td[1]/text()')
        l.add_xpath('price', '//div[@class="product-detail"]//span[@class="price "]/text()')
        l.add_xpath('stock', '//div[@class="product-detail"]//p[@class="product-option_stock"]/text()')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()