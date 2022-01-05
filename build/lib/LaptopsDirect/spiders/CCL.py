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

class CclSpider(CrawlSpider):
    name = 'CCL'
    custom_settings = { 
        'DOWNLOADER_MIDDLEWARES' : {
            'LaptopsDirect.middlewares.CustomProxyMiddleware': 350,
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 400,
        }
    }
    allowed_domains = ['cclonline.com']
    start_urls = ['https://www.cclonline.com']

    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//*[@id="incHeader_pnlDefaultMenu"]','//*[@id="ctl00_pnlPager"]',
        '//*[@id="pnlProductList"]/div[2]')), 
        callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        l.add_xpath('sku', '//*[@id="pnlPartNumber"]/span/text()')
        l.add_xpath('price', '//*[@id="pnlPriceText"]/p/span/text()')
        l.add_xpath('stock', '//*[@id="lblStock"]/text()')
        l.add_xpath('image_url', '//*[@id="imgPrimaryImage"]/@src')
        #l.add_xpath('description', '//div[@class="detail-panes"]')
        #l.add_xpath('description', '//div[@class="detail-panes"]')

        l.add_xpath('ean', '//*[@id="pnlHPSyndicateContent"]/script/@data-flix-ean')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()