# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem


class InsightSpider(SitemapSpider):
    name = 'Insight'
    allowed_domains = ['insight.com']
    sitemap_urls = ['https://www.insight.com/en_gb/sitemap/sitemap_product.xml']

    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title')
        l.add_xpath('sku', '//*[@id="prod-pres-price-box"]/ul/li[2]/h2/span/text()')
        l.add_xpath('price', '//*[@id="0007630954_price"]/span[1]/text()')
        l.add_xpath('product_title', '//*[@id="prod-pres-information"]/h1/span[1]')
        l.add_xpath('image_url', '//*[@id="prod-pres-gallery-image"]/img')
        l.add_xpath('description', '//*[@id="product-specification-tab"]')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()