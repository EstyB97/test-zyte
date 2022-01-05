# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem

class LaptopoutletSpider(SitemapSpider):
    name = 'LaptopOutlet'
    allowed_domains = ['laptopoutlet.co.uk']
    sitemap_urls = ['https://www.laptopoutlet.co.uk/robots.txt']
    
    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '//*[@id="top"]/head/title/text()')
        l.add_xpath('sku', '//*[@id="product_addtocart_form"]/div[3]/p/text()')
        l.add_xpath('price', '//*[@class="price-info"]/div/span/span/text()')
        l.add_xpath('product_title', '//*[@id="product_addtocart_form"]/div[3]/div[1]/span/text()')
        l.add_xpath('stock', '//*[@id="qty"]/@value')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()