# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import Join
import re

class AOCrawlSpider(CrawlSpider):
    name = 'AOCrawler'
    
    allowed_domains = ['ao.com']
    start_urls = ['https://ao.com/l/tvs/1/107-108/']
    DOMAIN_DEPTHS = {'ao.com': 1}
    
    custom_settings = { 
        'DEPTH_LIMIT': 2
    #    'DOWNLOADER_MIDDLEWARES' : {
    #        'LaptopsDirect.middlewares.CustomProxyMiddleware': 350,
    #        'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 400,
    #    }
    }

    
    rules = (
        Rule(LinkExtractor(allow=(), deny=(), restrict_xpaths=('//section//ul//li//a'
        
        )),
        callback='parse_item', follow=True),
        )

    def parse_item(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '//*[@id="Head"]/title/text()')
        l.add_xpath('sku', '//span[starts-with(.,"Belling")]/following::div[@class="feature"]//span[starts-with(.,"SKU")]/following::span[1]/text()', re=r"(\b.*)(!?\b)")
        l.add_xpath('sku', '//span[starts-with(.,"Stoves")]/following::div[@class="feature"]//span[starts-with(.,"SKU")]/following::span[1]/text()', re=r"(\b.*)(!?\b)")
        l.add_xpath('sku', '//div[@class="add-to-basket-btn"]/a/@data-productcode', re=r"[^_]*")
        l.add_xpath('sku', '//*[@id="main-skip-content"]/@data-product-sku', re=r"[^_]*")
        l.add_xpath('sku', '//*[@id="productSpecification"]//span[starts-with(.,"SKU")]/following::td[1]/span/text()', re=r"[^_]*")
        l.add_xpath('price', '//div[@class="price "]/span[@itemprop="price"]/@content')
        l.add_xpath('price', '//div[@class="price save-price"]/span[@itemprop="price"]/@content')
        l.add_xpath('price', '//span[@itemprop="price"]/@content')
        l.add_xpath('product_title', '//*[@id="pageTitle"]/text()')
        l.add_xpath('stock', '//span[@class="inStockText"]/text()')
        l.add_xpath('stock', '//span[@class="inStockText text-body"]/text()')
        l.add_xpath('stock', '//div[@data-tag-value="info-delivery"]/span[2]/text()')
        l.add_xpath('stock', '//span[@class="back-in-stock-soon__text"]/text()')
        l.add_xpath('stock', '//span[@class="inStockText text-body-sm"]/text()')
        l.add_xpath('stock', '//span[@itemprop="availability"]/following::span[1]/text()')
        l.add_xpath('stock', '//span[@itemprop="availability"]/@href')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()