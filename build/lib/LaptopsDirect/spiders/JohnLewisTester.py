# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import scrapy

class JohnlewisTestSpider(CrawlSpider):
    name = 'JohnLewis - Tester'
    allowed_domains = ['johnlewis.com']
    jl_base_url = 'https://www.johnlewis.com/electricals/c500001?page=%s'
    #start_urls = ['https://www.johnlewis.com/indesit-idc8t3b-ecotime-freestanding-condenser-tumble-dryer-8kg-load-b-energy-rating-white/p2275546?searchTerm=IDC8T3B']
    start_urls = [jl_base_url % 1]
    download_delay = 1.5

    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//nav[@aria-label="Categories menu"]',
        '//div[@class="product-list-container-right"]',
        '//li/a[@href="/electricals/c500001"]')), 
        callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        l.add_xpath('sku', '//dt[starts-with(.,"Manufacturer Part Number (MPN)")]/following::dd[1]/text()')
        l.add_xpath('sku', '//dt[starts-with(.,"Model name / number")]/following::dd[1]/text()')
        l.add_xpath('sku', '//div[@data-cy="product-specification-value-Model number"]/text()')
        #Catch all attempt from the URL, do not move up the list or will break successful SKUs which have a hyphen in the part code
        l.add_value('sku', response.url.split('-')[1])
        l.add_xpath('price', '//div[@class="standard-product-column-right"]//p[@class="price price--large"]/text()')
        l.add_xpath('price', '//div[@data-cy="product-price-title"]/span/text()')
        l.add_xpath('stock', '//*[@id="quantity"]/@value')
        l.add_xpath('stock', '//section[@data-cy="stock-availability"][1]/div[1]/text()')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()
    
    def parse(self, response):
        data = (response.body)
        if data['has_next']:
            next_page = data['page'] + 1
            yield scrapy.Request(self.jl_base_url % next_page)


#Code to allow multiple inheritancy

#from scrapy.linkextractors import LinkExtractor
#from scrapy.spiders import SitemapSpider, CrawlSpider, Rule

#class MySpider(SitemapSpider, CrawlSpider):
#    name = "myspider"
#    rules = ( Rule(LinkExtractor(allow=('', )), callback='parse_item', follow=True), )
#    sitemap_rules = [ ('/', 'parse_item'), ]
#    sitemap_urls = ['http://www.example.com/sitemap.xml']
#    start_urls = ['http://www.example.com']
#    allowed_domains = ['example.com']

#    def parse_item(self, response):
        # Do your stuff here
#        ...
        # Return to CrawlSpider that will crawl them
#        yield from self.parse(response)