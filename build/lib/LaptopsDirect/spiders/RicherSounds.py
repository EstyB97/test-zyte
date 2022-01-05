# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
from scrapy.loader.processors import Join
import re
from scrapy.linkextractors import LinkExtractor

class RicherSoundsSpider(SitemapSpider):
    name = 'richersounds'
    allowed_domains = ['richersounds.com']
    sitemap_urls = ['https://www.richersounds.com/robots.txt']

    #rules = (
    #    Rule(LinkExtractor(allow=(), restrict_xpaths=('//*[@id="om"]','//*[@id="maincontent"]//div[@class="column main"]')), 
    #    callback='parse_item', follow=True),
    #)

    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        l.add_xpath('sku', '//span[@class="manufacturer_model"]/text()')
        l.add_xpath('price', '//span[@data-price-type="finalPrice"]/@data-price-amount')
        l.add_xpath('stock', '//div[@title="Availability"]/span/text()')
        #l.add_xpath('image_url', '//*[@id="imgPrimaryImage"]/@src')
        #l.add_xpath('description', '//div[@class="detail-panes"]')
        #l.add_xpath('description', '//div[@class="detail-panes"]')

        #l.add_xpath('ean', '//*[@id="pnlHPSyndicateContent"]/script/@data-flix-ean')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()