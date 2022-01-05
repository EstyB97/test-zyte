# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
from scrapy.loader.processors import TakeFirst


class KikatekSpider(SitemapSpider):
    name = 'Kikatek'
    allowed_domains = ['kikatek.com']
    sitemap_urls = ['https://www.kikatek.com/Sitemap.products.xml.gz']
    handle_httpstatus_list = [301, 302, 200]

    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        l.add_xpath('sku', '//*[@id="Piper-Product-Heading"]/div/div[2]/h3/text()')
        l.add_xpath('price', '//*[@id="Piper-Product-Heading"]/div/div[2]/div[3]/div[1]/span[1]/text()')
        l.add_xpath('product_title', '//*[@id="Piper-Product-Heading"]/div/div[2]/h1/text()')
        l.add_xpath('stock', '//*[@id="Piper-Product-Heading"]/div/div[2]/div[3]/div[2]/span/text()')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()