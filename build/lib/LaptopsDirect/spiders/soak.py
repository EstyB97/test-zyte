# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem


class SoakSpider(SitemapSpider):
    name = 'soak'
    allowed_domains = ['soak.com']
    sitemap_urls = ['https://soak.com/robots.txt']

    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '//*[@id="Head"]/title/text()')
        l.add_xpath('sku', '//*[@id="product-content"]/div[2]/span/text()')
        l.add_xpath('price', '//*[@id="product-content"]/div[5]/div[1]/span/text()')
        l.add_xpath('product_title', '//*[@id="product-content"]/div[3]/h1/text()')
        l.add_xpath('image_url', '//*[@id="pdpMain"]/div[3]/div[1]/div[1]/div/div[1]/div[2]/div/div/div[1]/img[2]/@src')
        l.add_xpath('stock', '//*[@id="product-content"]/div[6]/ul/li[1]/p/strong/text()')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()