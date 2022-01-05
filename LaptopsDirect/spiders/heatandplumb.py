# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem


class heatandplumbSpider(SitemapSpider):
    name = 'heatandplumb'
    allowed_domains = ['heatandplumb.com']
    sitemap_urls = ['https://www.heatandplumb.com/sitemap/google-sitemap-products.xml']

    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '//*[@id="Head"]/title/text()')
        l.add_xpath('sku', '//*[@id="cart_form"]/div[3]/div[2]/div[1]/div/div/div[1]/label/text()')
        l.add_xpath('price', '//*[@id="cart_form"]/div[3]/div[2]/div[2]/div[1]/div/h2/text()')
        l.add_xpath('product_title', '//*[@id="cart_form"]/div[3]/div[2]/div[1]/div/div/div[1]/h1/text()')
        l.add_xpath('image_url', '//*[@id="cart_form"]/div[3]/div[1]/div[1]/div[1]/div[1]/div/div/div/img/@src')
        l.add_xpath('stock', '//span[@class="product-avl-stock-status"]/text()')
        l.add_xpath('stock', '//*[@id="cart_form"]/div[3]/div[2]/div[2]/div[1]/div/span[3]/text()')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()