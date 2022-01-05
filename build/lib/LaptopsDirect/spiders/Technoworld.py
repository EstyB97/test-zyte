# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem

class TechnoworldSpider(SitemapSpider):
    name = 'Technoworld'
    allowed_domains = ['technoworld.com']
    sitemap_urls = ['https://www.technoworld.com/robots.txt']
    
    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title')
        l.add_xpath('sku', '//div[@itemprop="sku"]/h2/b/text()')
        l.add_xpath('sku', '//meta[@itemprop="mpn"]/@content')
        l.add_xpath('price', '//meta[@property="product:price:amount"]/@content')
        l.add_xpath('price', '//*[@id="product_addtocart_form"]/div[2]/div[2]/div[1]/span[2]/span[2]/meta/@content')
        l.add_xpath('product_title', '//*[@id="product_addtocart_form"]/div[2]/div[1]/h1/span/text()')
        l.add_xpath('image_url', '//*[@id="image"]')
        l.add_xpath('stock', '//div[@title="Availability"]//text()')
        l.add_xpath('stock', '//*[@id="product_addtocart_form"]/div[2]/div[2]/p[2]/span/text()')
 
        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()
