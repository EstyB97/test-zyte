# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem


class boxspider(SitemapSpider):
    name = 'Box'
    allowed_domains = ['box.co.uk']
    custom_settings = {
        'USER_AGENT' : 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
        'COOKIES_ENABLED' : 'False',
        'DOWNLOAD_DELAY': '8', 
        'AUTOTHROTTLE_START_DELAY': '60',
        'AUTOTHROTTLE_MAX_DELAY': '800', 
        'AUTOTHROTTLE_TARGET_CONCURRENCY': '1.0', 
        'CLOSESPIDER_ERRORCOUNT': '500',
        'CONCURRENT_REQUESTS': '1',
        'ROBOTSTXT_OBEY' : 'True',
        'CLOSESPIDER_TIMEOUT' : '345600'
    }
    sitemap_urls = ['https://www.box.co.uk/sitemap/products-3.xml','https://www.box.co.uk/sitemap/products-1.xml','https://www.box.co.uk/sitemap/products-2.xml']

    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        #l.add_xpath('title', '//h2[@class="p-title-desc"]/text()')
        l.add_xpath('title', '/html/head/title/text()')
        l.add_xpath('sku', '//h1[@class="p-title-code"]/text()')
        l.add_xpath('sku', '//h2/span[@class="p-title-code"]/text()')
        l.add_xpath('price', '//div[@class="p-price"]/p[@class="p-price-inc"]/span[@class="pq-price"]/text()')
        l.add_xpath('price', '//tr[@class="p-cashback-pay"]/td/span/text()')
        l.add_xpath('description', '//*[@id="p-middle"]/div[2]/ul')
        l.add_xpath('stock', '//p[@class="p-stock"]/text()', re=r"(.+)")
        #OOS
        l.add_xpath('stock', '//div[@title="Request Stock Alert"]/text()', re=r"(.+)")
        
    

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()