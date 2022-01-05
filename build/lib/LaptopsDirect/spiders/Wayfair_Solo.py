# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import urlparse
import socket
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem

class WayfairSoloSpider(scrapy.Spider):
    name = 'Wayfair-Solo'
    custom_settings = { 
      'REDIRECT_ENABLED' : 'False',
   }
    allowed_domains = ['wayfair.co.uk']
    start_urls = ['https://www.wayfair.co.uk/storage-organisation/pdp/symple-stuff-storage-cabinet-jkd1343.html']

    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        l.add_xpath('product_title', '//*[@id="bd"]/div[2]/div/div[2]/div/div/div[1]/header/header/h1')
        l.add_xpath('sku', '//*[@id="bd"]/div[2]/div/div[2]/div/div/div[1]/header/p/a')
        l.add_xpath('price', '//*[@id="bd"]/div[2]/div/div[2]/div/div/div[2]/div/span')
        l.add_xpath('stock', '//*[@id="bd"]/div[2]/div/div[2]/div/div/div[4]/div')
        l.add_xpath('image_url', '//*[@id="bd"]/div[2]/div/div[1]/div[2]/div/div/div[1]/div/div[1]/div/div/ul/li[1]/div/div/div/div[1]/img/@src')
        l.add_xpath('description', '//*[@id="CollapsePanel-0"]')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()