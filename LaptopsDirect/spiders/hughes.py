# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
from scrapy.loader.processors import TakeFirst


class HughesSpider(SitemapSpider):
    name = 'hughes'
    allowed_domains = ['hughes.co.uk']
    sitemap_urls = ['https://www.hughes.co.uk/sitemap.xml']

    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '//*[@id="Head"]/title/text()')
        l.add_xpath('sku', '//div[@class="product--tab-box"]/@data-product')
        l.add_xpath('price', '//div[@class="product--tab-box"]/@data-value')
        l.add_xpath('price', '//span[@class="price--content content--default"]/text()')
        l.add_xpath('product_title', '//h2[@itemprop="name"]/text()')
        l.add_xpath('stock', '//div[@class="buybox--quantity block"]//div[@class="js--fancy-select-text"]/text()')
        l.add_xpath('stock', '//button[@class="gtm-product-buy-button buybox--button block btn is--primary is--center "]/text()')
        l.add_xpath('stock', '//div[@class="buybox--button-container block-group"]/button/@name')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()