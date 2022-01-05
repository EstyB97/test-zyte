# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class HappybedsSpider(CrawlSpider):
    name = 'happybedscrawl'
    allowed_domains = ['happybeds.co.uk']
    start_urls = ['https://www.happybeds.co.uk']

    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//*[@id="header-nav-container"]','//*[@id="page-content-wrapper"]')), 
        callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '//*[@id="Head"]/title/text()')
        l.add_xpath('price', '//*[@id="prod-pricing-inner"]/div/div[@class="prod-price-now 1"]/span/text()')
        l.add_xpath('product_title', '//*[@id="main-product-name"]/h1/text()')
        l.add_xpath('stock', '//*[@id="btn-cart-view"]/span/span')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()