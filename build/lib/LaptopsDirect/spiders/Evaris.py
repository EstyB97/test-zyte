# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem


class EvarisSpider(SitemapSpider):
    name = 'Evaris'
    allowed_domains = ['evaris.com']
    sitemap_urls = ['https://www.evaris.com/shop/sitemap.xml']

    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '//*[@id="top"]/head/title')
        l.add_xpath('sku', '//div[@class="sku"]/text()')
        l.add_xpath('price', '//div[@class="price-box"]/span[@class="price-including-tax"]/span[@class="price"]/text()')
        l.add_xpath('stock', '//div[@class="stock"]/p/span[@class="value"]/text()')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()

# Evaris seem to be employing throttling on their website that only allows so many requests during a certain period. 
# Need to look into what their limit is and if it might be beneficial to set this up as a really slow crawl or look to use multiple IPs on rotation to get the results.
# Limit number is 200x in a period of around 5-10 minutes, but the site lets you hit it at any rate