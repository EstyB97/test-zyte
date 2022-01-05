# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class ScrewfixSpider(CrawlSpider):
    name = 'ScrewFix'
    allowed_domains = ['screwfix.com']
    start_urls = ['https://www.screwfix.com/c/bathrooms-kitchens/cat810412','https://www.screwfix.com/c/security-ironmongery/cctv-surveillance/cat810224']

    rules = (
        Rule(LinkExtractor(allow=()), callback='parse_item', follow=True),
        Rule(LinkExtractor(deny=(r'^https:\/\/www\.screwfix\.com\/jsp(.*?)',r'^https:\/\/www\.screwfix\.com\/search(.*?)',r'\?')), follow=False),
    )

    def parse_item(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        l.add_xpath('sku', '//*[@id="product_code_container"]/span/text()')
        l.add_xpath('price', '//div[@class="row pr__prices"]//input/@value')
        l.add_xpath('stock', '//input[@id="qty"]/@value')


        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()