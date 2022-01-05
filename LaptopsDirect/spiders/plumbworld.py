# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
from scrapy.loader.processors import TakeFirst


class PlumbWorldSpider(SitemapSpider):
    name = 'plumbworld'
    allowed_domains = ['plumbworld.co.uk']
    sitemap_urls = ['https://www.plumbworld.co.uk/robots.txt']

    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        l.add_xpath('sku', '//figure/figcaption/text()')
        l.add_xpath('price', '/html/head/meta[@property="product:price:amount"]/@content')
        l.add_xpath('product_title', '//*[@id="productDisplayName"]/text()')
        l.add_xpath('stock', '//div[@class="wrapper"]/figure/text()')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()