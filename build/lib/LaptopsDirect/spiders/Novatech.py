# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem

class NovatechSpider(SitemapSpider):
    name = 'Novatech'
    allowed_domains = ['novatech.co.uk']
    sitemap_urls = ['https://www.novatech.co.uk/sitemap-products.xml']
    
    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '//html/head/title/text()')
        l.add_xpath('sku', '//p[@class="stock-codes"][2]/span/text()')
        l.add_xpath('sku', '/html/body/div[7]/div/div[2]/div[1]/div[3]/div[2]/p[2]/span/text()')
        l.add_xpath('price', '//*[@id="newspec-pricesection"]/div/p[2]/span[2]/text()')
        l.add_xpath('product_title', '//*[@id="newspec-prodname"]/h1')
        l.add_xpath('image_url', '//*[@id="newspec-imageblock"]/center/div/div/img')
        l.add_xpath('description', '//*[@id="overview"]/div')
        l.add_xpath('stock', '//*[@id="newspec-pricesection"]/a/text()')
            
        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()