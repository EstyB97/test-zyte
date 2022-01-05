# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
from scrapy.loader.processors import TakeFirst


class SonicdirectSpider(SitemapSpider):
    name = 'sonicdirect'
    allowed_domains = ['sonicdirect.co.uk']
    sitemap_urls = ['https://www.sonicdirect.co.uk/sitemap.xml']

    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '//*[@id="Head"]/title/text()')
        l.add_xpath('sku', '//meta[@property="og:image"]/@content')
        #l.add_xpath('sku', '//*[@id="fmAdd2Cart"]//@data-flix-mpn')
        l.add_xpath('price', '/html/head/meta[@property="og:price:amount"]/@content')
        l.add_xpath('product_title', '//*[@id="fmAdd2Cart"]/div[1]/div[2]/h1/text()')
        l.add_xpath('stock', '//*[@id="AddToBasket"]/@value')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()