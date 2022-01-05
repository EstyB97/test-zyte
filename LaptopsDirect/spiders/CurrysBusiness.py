# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
import logging

class CurrysBusinessSpider(SitemapSpider):
    name = 'Currys Business'
    custom_settings = { 
        'DOWNLOADER_MIDDLEWARES' : {
            'LaptopsDirect.middlewares.CustomProxyMiddleware': 350,
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 400,
        } 
   }
    allowed_domains = ['currys.co.uk']
    sitemap_urls = ['https://www.currys.co.uk/robots.txt']
    #handle_httpstatus_list = [301, 302, 200]
    
    def parse(self, response):

        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        #if response.xpath('//*[@id="content"]/div[2]/section/div[2]/h1/span[1][starts-with(.,"INDESIT")'):
       #     item['promo_price'] = extract_with_css('span.price-num:last-child::text')
       # else:
       #     item['promo_price'] = extract_with_css('.product-highlight-label::text')




        l.add_xpath('sku', '//*[@id="content"]/div[2]/section/div[2]/h1/span[1][starts-with(.,"INDESIT")]/following::span[1]/text()')



        l.add_xpath('sku', '//meta[@property="og:title"]/@content')
        l.add_xpath('sku', '//meta[@property="twitter:title"]/@content')
        l.add_xpath('sku', '//*[@id="content"]/div[2]/section/div[2]/h1/span[2]/text()')
        l.add_xpath('price', '//meta[@property="og:price:amount"]/@content')
        l.add_xpath('price', '//meta[@property="twitter:data1"]/@content')          
        l.add_xpath('price', '//div[@class="amounts"]/div/div/span/text()')
        l.add_xpath('stock', '//li[@id="delivery"]//text()')
        l.add_xpath('stock', '//meta[@property="twitter:data2"]/@content')
        l.add_xpath('pcwb_product_code', '//p[@class="prd-code"]/text()')
            
        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()