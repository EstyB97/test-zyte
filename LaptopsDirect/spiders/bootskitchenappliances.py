# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
from scrapy.loader.processors import TakeFirst

class BootskitchenappliancesSpider(SitemapSpider):
    name = 'bootskitchenappliances'
    allowed_domains = ['bootskitchenappliances.com']
    sitemap_urls = ['https://www.bootskitchenappliances.com/robots.txt']
    default_output_processor = TakeFirst()

    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)
        
        #Scrape Fields
        l.add_xpath('title', '//*[@id="Head"]/title/text()')
        l.add_xpath('sku', '//*[@id="product"]//@productcode')
        l.add_xpath('price', '//*[@id="product"]/div/div[6]/div[2]/span/div/text()')
        l.add_xpath('product_title', '//*[@id="pageTitle"]/text()')
        l.add_xpath('image_url', '//*[@id="mediumImage1"]/@src')
        l.add_xpath('stock', '//div[@class="action"]//div[@class="DeliveryOptions"]/div/p/text()')
        l.add_xpath('stock', '//section[@id="product"]//div[@id="prodMedia"]//h2/text()')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()