# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem


class Aircon247Spider(SitemapSpider):
    name = 'aircon247'
    allowed_domains = ['aircon247.com']
    sitemap_urls = ['https://www.aircon247.com/sitemap.xml']

    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        l.add_xpath('sku', '//*[@id="MainContent"]/section[1]/div/div[2]/div/div[2]/div/p/span')
        l.add_xpath('price', '//*[@class="our-price"]/text()')
        l.add_xpath('product_title', '//*[@id="tdCenter"]/div/div/table/tbody/tr/td/div/div/div/div/table/tbody/tr/td/div/div/div/form/div/table[1]/tbody/tr/td[2]/table/tbody/tr[1]/td/h2/div/text()')
        l.add_xpath('image_url', '//*[@id="rabbit"]/img')
        l.add_xpath('stock', '//*[@id="btn_AddToBasket"]/text()')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()