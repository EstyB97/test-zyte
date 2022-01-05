# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem


class AirconcentreSpider(SitemapSpider):
    name = 'airconcentre'
    allowed_domains = ['airconcentre.co.uk']
    sitemap_urls = ['http://airconcentre.co.uk/robots.txt']

    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        l.add_xpath('sku', '//p[starts-with(.,"Quick Find Code:")]/span/text()')
        l.add_xpath('price', '//meta[@property="og:price:amount"]/@content')
        l.add_xpath('product_title', '//div[@class="content"]/h1/text()')
        l.add_xpath('stock', '//span[@class="icon addToCartIcon"]/following::span[1]/text()')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()