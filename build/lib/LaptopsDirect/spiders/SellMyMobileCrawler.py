# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.loader import ItemLoader
from LaptopsDirect.items import MobilePhoneItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class SellmymobilecrawlerSpider(CrawlSpider):
    name = 'SellMyMobileCrawler'
    allowed_domains = ['sellmymobile.com']
    start_urls = ['https://www.sellmymobile.com/phones/']

    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('/html/body/main')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        l = ItemLoader(item=MobilePhoneItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        l.add_xpath('sku', '//*[@id="results_hero"]/div/div/div/h1/span/text()')
        l.add_xpath('price', '//*[@id="device_results_table_body"]/tr[1]/td[5]/span[1]/text()')
        l.add_xpath('recycler', '//*[@id="device_results_table_body"]/tr[1]/td[1]/img/@alt')
        l.add_xpath('numberofdeals', '//*[@id="sidebar"]/header/h3/span/text()')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()