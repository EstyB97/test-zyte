# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
import socket
import re
from scrapy.spiders import SitemapSpider, Rule
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
from scrapy.loader.processors import TakeFirst
from scrapy.linkextractors import LinkExtractor


class JohnlewisSpider(SitemapSpider):
    name = 'JohnLewis'
    custom_settings = { 
      'DOWNLOAD_DELAY': '0.08', 
      'AUTOTHROTTLE_START_DELAY': '4',
      'AUTOTHROTTLE_MAX_DELAY': '80', 
      'AUTOTHROTTLE_TARGET_CONCURRENCY': '16', 
      'CLOSESPIDER_ERRORCOUNT': '500',
      'CONCURRENT_REQUESTS': '24',
      'DOWNLOADER_MIDDLEWARES' : {
            'LaptopsDirect.middlewares.CustomProxyMiddleware': 350,
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 400,
        },
      #'USER_AGENT' : 'AdsBot-Google'
   }
    allowed_domains = ['johnlewis.com']
    #sitemap_urls = ['https://www.johnlewis.com/product-1.xml', 'https://www.johnlewis.com/product-2.xml', 'https://www.johnlewis.com/product-3.xml']
    sitemap_urls = ['https://www.johnlewis.com/robots.txt']
    sitemap_follow = ["^https://www.johnlewis.com/products.*$"]

    def parse(self, response,meta={"proxy":"41.65.252.101:1981"}):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        #Look for HOTPOINT in product title, Extract everything between Aquarius and fullstop9 for Ovens
        l.add_xpath('sku', '//h1[starts-with(.,"Hotpoint Aquarius")]', re=r"(?<=Aquarius)(.*)(?=.9)")
        l.add_xpath('sku', '//dt[starts-with(.,"Manufacturer Part Number (MPN)")]/following::dd[1]/text()')
        l.add_xpath('sku', '//dt[starts-with(.,"Model name / number")]/following::dd[1]/text()')
        l.add_xpath('sku', '//div[@data-cy="product-specification-value-Model number"]/text()')
        l.add_xpath('sku', '//div[@data-cy="product-specification-value-Product code"]/text()')
        #Catch all attempt from the URL, do not move up the list or will break successful SKUs which have a hyphen in the part code
        l.add_value('sku', response.url.split('-')[1])
        l.add_xpath('price', '//div[@class="standard-product-column-right"]//p[@class="price price--large"]/text()')
        l.add_xpath('price', '//div[@data-cy="product-price-title"]/span/text()')
        l.add_xpath('stock', '//*[@id="quantity"]/@value')
        l.add_xpath('stock', '//div[@data-cy="stock"]/text()')
        l.add_xpath('stock', '//section[@data-cy="stock-availability"][1]/h3/text()')
        l.add_xpath('stock', '//button[@data-test="add to basket"]/text()')
        #Handling for OOS John Lewis items using the notify me email box that appears on OOS
        l.add_xpath('stock', '//section[@data-cy="email-me"]/h2/text()')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        #l.replace_value('stock','10', re=r"Add to your basket")
        return l.load_item()