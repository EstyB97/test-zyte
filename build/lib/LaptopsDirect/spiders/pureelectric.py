# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
from scrapy.loader.processors import TakeFirst

class PureelectricSpider(SitemapSpider):
    name = 'purelectric'
    custom_settings = { 
        'DOWNLOADER_MIDDLEWARES' : {
            'LaptopsDirect.middlewares.CustomProxyMiddleware': 350,
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 400,
        }
    }
    allowed_domains = ['pureelectric.com']
    sitemap_urls = ['https://www.pureelectric.com/sitemap.xml']
    default_output_processor = TakeFirst()

    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)
        
        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        l.add_xpath('price', '//span[@data-product-price]/text()')
        #l.add_xpath('product_title', '///*[@id="shopify-section-product-form"]/div[2]/div[1]/div/h1/text()')
        #l.add_xpath('sku', '//*[@id="shopify-section-product-images"]/div[2]/div/div/div[1]/div/div/@src')
        l.add_xpath('stock', '//span[@class="product-instock__text"]/text()')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()