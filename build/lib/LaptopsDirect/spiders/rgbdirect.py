# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem


class RgbSpider(SitemapSpider):
    name = 'rgbdirect'
    allowed_domains = ['rgbdirect.co.uk']
    sitemap_urls = ['https://www.rgbdirect.co.uk/robots.txt']

    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '//*[@id="Head"]/title/text()')
        l.add_xpath('sku', '//span[@itemprop="name"]/text()')
        l.add_xpath('price', '//*[@id="price"]/span[@itemprop="price"]/text()')
        l.add_xpath('stock', '//div[@id="price"]//*[(@itemprop="availability") or (@itemprop="itemCondition")]/@content')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()