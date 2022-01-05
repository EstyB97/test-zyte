# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class ComputerpiratesSpider(CrawlSpider):
    name = 'computerpirates'
    allowed_domains = ['computerpirates.co.uk']
    start_urls = ['https://computerpirates.co.uk/catalog/category/view/s/laptops-uk-qwerty/id/1177/']

    #rules = (
        #Rule(LinkExtractor(allow=(), restrict_xpaths=('/html/body/div[2]/div/div[5]/div')), 
        #callback='parse_item', follow=True),
    #)

    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('/html')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        l.add_xpath('sku', '//*[@id="product_addtocart_form"]/div[3]/div[2]/div[1]/h1/text()')
        #l.add_xpath('price', '//*[@id="main-content"]/div/div[3]/form/div/div[1]/div[1]/p/text()')
        #l.add_xpath('product_title', '//*[@id="product_addtocart_form"]/div[3]/div[2]/div[1]/h1/text()')
        #l.add_xpath('image_url', '//*[@id="main-content"]/div/div[2]/div[1]/div[6]/div[1]/div[1]/a/img')
        #l.add_xpath('description', '//*[@id="main-content"]/div/div[2]/div[3]')
        #l.add_xpath('stock', '//*[@id="main-content"]/div/div[3]/form/div/ul/li[1]/span/text()')

        #Monitored Attribute on this scrape?
        l.add_xpath('monitoredcategory', '/html/body/div[1]/div[1]/div[2]/a/span/text()')
        l.add_xpath('monitoredattribute', '//*[@id="product-attribute-specs-table"]/tbody/tr[1]/th[starts-with(.,"EAN")]/following::td[1]/text()')
        l.add_xpath('monitoredattribute2', '//*[@id="product-attribute-specs-table"]/tbody/tr[2]/th[starts-with(.,"SKU")]/following::td[1]/text()')
          
        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()
