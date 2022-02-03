# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
from scrapy.loader.processors import Join
import re
from scrapy.linkextractors import LinkExtractor


class AoSpider(SitemapSpider):
    name = 'AO'
    #custom_settings = { 
        #'DOWNLOADER_MIDDLEWARES' : {
        #    'LaptopsDirect.middlewares.CustomProxyMiddleware': 350,
        #    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 400,
        #}
   # }
    rotate_user_agent = True
    allowed_domains = ['ao.com']
    sitemap_urls = ['https://ao.com/sitemaps/product/toc.xml', 'https://ao.com/sitemaps/product/Dishwashers-21.xml', 'https://ao.com/sitemaps/product/Computing-250.xml']

    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        #l.add_xpath('title', '//h1[@id="pageTitle"]/text()')
        l.add_xpath('title', '//*[@id="Head"]/title/text()')
        l.add_xpath('sku', '//span[starts-with(.,"Belling")]//following::div[@data-tag-name="sku"]/following::span[1]/text()')
        l.add_xpath('sku', '//span[starts-with(.,"Stoves")]//following::div[@data-tag-name="sku"]/following::span[1]/text()')
        #does the regex need to be in there for the below addition, first one to check if coverage drop, matching up to first _ in the regex...
        l.add_xpath('sku', '//div[@data-tag-name="sku"]/following::span[1]/text()', re=r"[^_]*")
        l.add_xpath('sku', '//div[@class="add-to-basket-btn"]/a/@data-productcode', re=r"[^_]*")
        l.add_xpath('sku', '//*[@id="main-skip-content"]/@data-product-sku', re=r"[^_]*")
        l.add_xpath('sku', '//*[@id="productSpecification"]//span[starts-with(.,"SKU")]/following::td[1]/span/text()', re=r"[^_]*")
        l.add_xpath('sku', '//title/text()', re=r"^.+?(?=\|)")
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
        l.add_xpath('stock', '//div[@class="back-in-stock"]/h3/text()')
        l.add_xpath('stock', '//span[@class="text-title"]/text()')
        


        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()