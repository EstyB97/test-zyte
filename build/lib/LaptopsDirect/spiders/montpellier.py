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


class MontpellierSpider(SitemapSpider):
    name = 'montpellier'
    allowed_domains = ['montpellier-appliances.com']
    sitemap_urls = ['https://www.montpellier-appliances.com/product_listing-sitemap.xml']

    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '//html/head/title/text()')
        l.add_xpath('sku', '//html/head/title', re=r"^(?:[^\s]*\s){1}([^\s]*)")
        l.add_xpath('price', '//div[@class="srp"]/text()')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()