# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class DehumidifiersukSpider(CrawlSpider):
    name = 'dehumidifiersuk'
    allowed_domains = ['dehumidifiersuk.com']
    start_urls = ['https://www.dehumidifiersuk.com']

    rules = (
        Rule(LinkExtractor(allow=()), 
        callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        l.add_xpath('sku', '//meta[@name="keywords"]/@content')
        l.add_xpath('price', '//p[@class="special-price"]')
        l.add_xpath('stock', '//*[@id="product_addtocart_form"]/div[2]/div[1]/div/p[2]/span/text()')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()