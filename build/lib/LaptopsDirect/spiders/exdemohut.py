# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem

class ExdemohutSpider(SitemapSpider):
    name = 'Exdemohut'
    allowed_domains = ['exdemohut.com']
    sitemap_urls = ['https://exdemohut.com/sitemap.xml'] 

    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '//*[@id="html-products"]/head/title')
        l.add_xpath('sku', '//*[@id="js-product-reference"]/text()')
        l.add_xpath('price', '//*[@id="product_addtocart_form"]/div[3]/div[3]/div/div/span[1]/span[2]/text()')
        l.add_xpath('product_title', '//*[@id="product_addtocart_form"]/div[3]/div[1]/h1/text()')
        l.add_xpath('image_url', '//*[@id="js-product-image"]/div[1]/div[2]/div/div/div[1]/a/img')
        l.add_xpath('description', '//*[@id="product-tabs"]/div/div[1]')
        l.add_xpath('stock', '//*[@id="product_addtocart_form"]/div[3]/div[3]/div/p/span/text()')  
        l.add_xpath('category', '//*[@id="root-wrapper"]/div/div/div[2]/div[2]/div/div[1]/ul/li[2]/a/span')

        # Spec
        l.add_xpath('processor', '//*[@id="product-attribute-specs-table-3"]/tbody/tr[2]/td/text()')
        l.add_xpath('processormodel', '//*[@id="product-attribute-specs-table-3"]/tbody/tr[3]/td/text()') 
        l.add_xpath('ram', '//*[@id="product-attribute-specs-table-4"]/tbody/tr[1]/td/text()')    
        l.add_xpath('harddrive', '//*[@id="product-attribute-specs-table-5"]/tbody/tr[1]/td/text()')          
        
        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


        return l.load_item()