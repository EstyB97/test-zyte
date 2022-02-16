# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
import logging

class SimplyelectricalsSpider(SitemapSpider):
    name = 'simplyelectricals'
    allowed_domains = ['simplyelectricals.co.uk']
    sitemap_urls = ['https://www.simplyelectricals.co.uk/robots.txt']
    handle_httpstatus_list = [301, 302, 200]
    
    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        l.add_xpath('sku', '//div[@class="sku"]/text()')
        l.add_xpath('price', '//meta[@itemprop="price"]/@content')   
        l.add_xpath('stock', '//*[@id="buy-now-tab-link"]/text()')
                    
        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()