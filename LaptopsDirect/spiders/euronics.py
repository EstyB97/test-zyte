# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem


class EuronicsSpider(SitemapSpider):
    name = 'euronics-uk'
    allowed_domains = ['euronics.co.uk']
    sitemap_urls = ['https://www.euronics.co.uk/robots.txt']

    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        l.add_xpath('sku', '//div[@class="product-code"]/text()')
        l.add_xpath('price', '//div[@class="sections__area sections__area--half"]//li[@class="prd-price__now"]/span')
        #l.add_xpath('stock', '//*[@id="pdpAddtoCartInput"]/@value')
        l.add_xpath('stock', '//i[@class="icon icon--in-stock"]/@class')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()