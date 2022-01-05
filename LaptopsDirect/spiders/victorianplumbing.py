# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem


class VictorianplumbingSpider(SitemapSpider):
    name = 'victorianplumbing'
    allowed_domains = ['victorianplumbing.co.uk']
    sitemap_urls = ['https://www.victorianplumbing.co.uk/products.xml']

    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '//*[@id="Head"]/title/text()')
        l.add_xpath('sku', '//select[@id="ddlProdSelSingle"]/option')
        l.add_xpath('sku', '//meta[@itemprop="sku"]/@content')
        l.add_xpath('sku', '//*[@id="lblProdCodeMain"]/text()')
        l.add_xpath('price', '//*[@id="ctl00_Middle_ctl00_lblIncPrice"]/text()')
        l.add_xpath('product_title', '//*[@id="h1ProdName"]/text()')
        l.add_xpath('image_url', '//*[@id="prodImgCarousel"]/div[1]/div/div[1]/div/a/img/@src')
        l.add_xpath('stock', '//div[@id="prodStock"]//text()')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()