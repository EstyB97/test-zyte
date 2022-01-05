# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem


class ApplianceworldSpider(SitemapSpider):
    name = 'applianceworld'
    allowed_domains = ['applianceworldonline.com']
    sitemap_urls = ['https://www.applianceworldonline.com/sitemap.xml']

    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        l.add_xpath('sku', '/html/head/title', re=r"^(?:[^\s]*\s){1}([^\s]*)")
        l.add_xpath('price', '//div[@class="price-box"]//span[contains(@id, "product-price-")]/span[@class="price"]/text()')
        l.add_xpath('stock', '//*[@id="product-shop-container"]//span[@class="customstatus"]/text()')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()