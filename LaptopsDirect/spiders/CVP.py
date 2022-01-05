# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class CvpSpider(CrawlSpider):
    name = 'CVP'
    allowed_domains = ['cvp.com']
    start_urls = ['https://cvp.com/']

    rules = (
        Rule(LinkExtractor(allow=()),callback='parse_item',follow=True),
        Rule(LinkExtractor(allow=(r'^https:\/\/www\.cvp\.com\/catalogue(.*?)',r'^https:\/\/www\.cvp\.com\/department(.*?)',r'^https:\/\/www\.cvp\.com\/product(.*?)',r'^https:\/\/cvp\.com\/catalogue(.*?)',r'^https:\/\/cvp\.com\/department(.*?)',r'^https:\/\/cvp\.com\/product(.*?)'))),
    )

    def parse_item(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        l.add_xpath('sku', '//*[@id="p_pc"]/text()')
        l.add_xpath('price', '(//div[@class="product_pricing"]/div[@id="vat_price"]/text())[1]')
        l.add_xpath('product_title', '//*[@id="product_page"]/section[1]/div[1]/div/h1/text()')
        l.add_xpath('stock', '//*[@id="stock_message"]/span[2]/text()')
            
        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()