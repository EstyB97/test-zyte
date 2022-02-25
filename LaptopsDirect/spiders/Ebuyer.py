# -*- coding: utf-8 -*-
from datetime import datetime
from scrapy.http.request import Request
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
import logging

class EbuyerSpider(SitemapSpider):
    name = 'Ebuyer'
    custom_settings = { 
        'DOWNLOADER_MIDDLEWARES' : {
            'LaptopsDirect.middlewares.CustomProxyMiddleware': 350,
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 400,
            #'LaptopsDirect.middlewares.RotatingProxyMiddleware': 610,
            #'LaptopsDirect.middlewares.BanDetectionMiddleware': 620,
        },
        'CLOSESPIDER_TIMEOUT' : '864000'
    }
    allowed_domains = ['ebuyer.com']
    sitemap_urls = ['https://www.ebuyer.com/sitemaps/web-sitemap-index.xml', 'https://www.ebuyer.com/sitemaps/products-13.xml.gz']
    sitemap_follow = ["^https://www.ebuyer.com/sitemaps/products.*$"]
    
    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        l.add_xpath('sku', '//*[@id="main-content"]/div/div/div[1]/div[1]/span[2]/text()')
        #l.add_xpath('price', '//div[@class="purchase-info__price"]/div[@class="ex-vat"]/p/text()')
        l.add_xpath('price', '//meta[@name="twitter:data1"]/@content') #captures the same price as above, but returns a value when the stock level is 0
        l.add_xpath('product_title', '//*[@id="main-content"]/div/div[2]/div[1]/h1/text()')
        #l.add_xpath('image_srcx', '//div[@class="image-gallery__hero"]/a/img/@src')
        #l.add_xpath('description', '//div[@class="product-description product-description--collapsible"]')
        l.add_xpath('stock', '//div[@class="purchase-info__cta"]/form/div/input/@min')
        l.add_xpath('stock', '//button[@data-pre-text="Notify me"]/text()') #this updates to 0 stock level on OOS items
        l.add_xpath('stock','//div[@class="purchase-info"]/div/h2/text()') #this updates to 0 stock level on call for pricing items

        #Monitored Attribute on this scrape?
        #l.add_xpath('slotsqty', '//*[@id="technical-specification"]/table/tbody/tr/td[starts-with(.,"Slots Qty")]/following::td[1]/text()')
        #l.add_xpath('emptyslots', '//*[@id="technical-specification"]/table/tbody/tr/td[starts-with(.,"Empty Slots")]/following::td[1]/text()')
        #l.add_xpath('imagebrightness', '//*[@id="technical-specification"]/table/tbody/tr/td[starts-with(.,"Image Brightness")]/following::td[1]/text()')
                  
        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()