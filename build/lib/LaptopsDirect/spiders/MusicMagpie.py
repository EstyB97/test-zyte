# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.loader import ItemLoader
from LaptopsDirect.items import MobilePhoneItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class MusicmagpieSpider(CrawlSpider):
    name = 'MusicMagpie'
    allowed_domains = ['musicmagpie.co.uk']
    start_urls = ['http://musicmagpie.co.uk/']

    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('/html')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        l = ItemLoader(item=MobilePhoneItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        l.add_xpath('sku', '//*[@id="ctl00_ctl00_ctl00_ContentPlaceHolderDefault_mainContent_itemCondition3_10_lblItemDescription"]/text()')
        l.add_xpath('price', '//*[@id="ctl00_ctl00_ctl00_ContentPlaceHolderDefault_mainContent_itemCondition3_10_lblPrice"]/text()')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()