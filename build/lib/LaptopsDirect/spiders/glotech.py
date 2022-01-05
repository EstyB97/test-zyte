# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class GlotechSpider(CrawlSpider):
    name = 'glotech'
    allowed_domains = ['glotech.co.uk']
    start_urls = ['https://www.glotech.co.uk/appliances/']

    rules = (
        Rule(LinkExtractor(allow=(r'^https:\/\/www\.glotech\.co\.uk\/appliances(.*?)'),restrict_xpaths=('/html/body//ul[@class="nav navbar-nav"]',
        '//div[@class="content container"]//div[@class="col-md-9 col-sm-8"]',
        '//div[@class="container content"]//div[@class="sorting-block margin-bottom-20"]')),callback='parse_item',follow=True),
    )

    def parse_item(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        l.add_xpath('sku', '//*[@id="information"]//table//tr/td[starts-with(.,"Product Code")]/following::td[1]/text()')
        l.add_xpath('price', '//*[@id="add"]/@price')
        l.add_xpath('stock', '//*[@id="add"]/@qty')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()