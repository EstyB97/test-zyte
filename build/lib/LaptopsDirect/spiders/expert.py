# -*- coding: utf-8 -*-
#from datetime import datetime
#import urlparse
#import urllib.parse
#import socket
#from scrapy.spiders import SitemapSpider
#from scrapy.loader import ItemLoader
#from LaptopsDirect.items import LaptopsdirectItem
#from scrapy.loader.processors import TakeFirst


#class ExpertSpider(SitemapSpider):
#    name = 'expert'
#    allowed_domains = ['expert.ie']
#    sitemap_urls = ['https://www.expert.ie/googlesitemap.xml']

#    def parse(self, response):
#        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
#        l.add_xpath('title', '//*[@id="Head"]/title/text()')
#        l.add_xpath('sku', '//strong[@itemprop="mpn"]/text()')
#        l.add_xpath('price', '//span[@class="TotalPrice"]/text()')
#        l.add_xpath('product_title', '//h1[@itemprop="name"]/text()')
#        l.add_xpath('stock', '//p[@class="delivery"]/text()')

        # Administration Fields
#        l.add_value('url', response.url)
#        l.add_value('project', self.settings.get('BOT_NAME'))
#        l.add_value('useragent', self.settings.get('USER_AGENT'))
#        l.add_value('spider', self.name)
#        l.add_value('server', socket.gethostname())
#        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

#        return l.load_item()


# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class ExpertSpider(CrawlSpider):
    name = 'expert'
    allowed_domains = ['expert.ie']
    start_urls = ['https://www.expert.ie']

    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=()), 
        callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '//*[@id="Head"]/title/text()')
        l.add_xpath('sku', '//strong[@itemprop="mpn"]/text()')
        l.add_xpath('price', '//span[@class="TotalPrice"]/text()')
        l.add_xpath('product_title', '//h1[@itemprop="name"]/text()')
        l.add_xpath('stock', '//p[@class="delivery"]/text()')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()