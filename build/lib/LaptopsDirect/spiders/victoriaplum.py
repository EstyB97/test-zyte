# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem


class VictoriaplumSpider(SitemapSpider):
    name = 'victoriaplum'
    allowed_domains = ['victoriaplum.com']
    sitemap_urls = ['https://victoriaplum.com/sitemap/section/product']

    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '//*[@id="Head"]/title/text()')
        l.add_xpath('sku', '//span[@class="product__code i-active-csi"]/@data-csi')
        l.add_xpath('price', '//span[@class="price  price--reduced "]/text()')
        l.add_xpath('stock', '//span[@class="stock-message-availability"]/text()')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()