# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem


class AppliancecitySpider(SitemapSpider):
    name = 'appliancecity'
    custom_settings = { 
      'CLOSESPIDER_ERRORCOUNT': '500',
   }
    allowed_domains = ['appliancecity.co.uk']
    sitemap_urls = ['https://www.appliancecity.co.uk/robots.txt']
    

    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        l.add_xpath('sku', '//div[@class="acity-product-trustpilot-widget acity-product-single-trustpilot-widget trustpilot-widget"]/@data-sku')
        l.add_xpath('price', '//h1/following::p[1]/span/bdi/text()')
        l.add_xpath('price', '//div[@class="single-product-infos"]/div/p/span/text()')
        l.add_xpath('price', '//p[@class="price"]/span[@class="woocommerce-Price-amount amount"]/text()')
        l.add_xpath('stock', '//div[@class="acity-product-availability acity-product-availability-in-stock acity-product-single-availability"]/text()')
        l.add_xpath('stock', '//p[@class="price"]/following::div[1]/text()')
        #zero-er line for this item is no longer available pages
        l.add_xpath('stock', '//p[@class="acity-product-strapline acity-product-single-strapline"]/text()')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()