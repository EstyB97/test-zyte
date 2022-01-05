# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class JohnlewisCrawlSpider(CrawlSpider):
    name = 'JohnLewis - 2'
    allowed_domains = ['johnlewis.com']
    #start_urls = ['https://www.johnlewis.com/indesit-idc8t3b-ecotime-freestanding-condenser-tumble-dryer-8kg-load-b-energy-rating-white/p2275546?searchTerm=IDC8T3B']
    start_urls = ['https://www.johnlewis.com/aeg-steambake-bes355010m-single-built-in-electric-steam-oven-a-energy-rating-stainless-steel/p4323046','https://www.johnlewis.com/electricals/c500001', 'https://www.johnlewis.com/electricals/cooking/c6000046', 'https://www.johnlewis.com/browse/electricals/cooking/cookers/belling/_/N-adkZ1z13xzy']

    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//nav[@aria-label="Categories menu"]',
        '//div[@class="product-list-container-right"]',
        '//ul[@aria-label="Available colours"]',
        '//div[@class="faceted-filters-accordion"]/h2/button[starts-with(.,"Brand")]',
        '//li/a[@href="/electricals/c500001"]')), 
        callback='parse_item', follow=True),
    )

    def parse_item(self, response):
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
        l.add_xpath('stock', '//section[@data-cy="stock-availability"][1]/h3/text()')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()