# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
import logging

class BetterbathroomsbidSpider(SitemapSpider):
    name = 'betterbathroomsbid'
    allowed_domains = ['betterbathrooms.com']
    sitemap_urls = ['https://www.betterbathrooms.com/sitemaps/sitemap-index.xml']
    
    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('price', '//*[@id="topcontent"]/div[2]/span[2]/img/@alt')
            
        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()