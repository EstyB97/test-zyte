# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
from LaptopsDirect.items import BookItem
import logging
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import scrapy

class EbuyerimagesSpider(SitemapSpider):
    name = 'EbuyerImages'
    allowed_domains = ['ebuyer.com']
    sitemap_urls = ['https://ebuyer.com/robots.txt']

    custom_settings = {
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
    }

    def parse(self, response):

        #for elem in response.xpath("//img"):
        #    img_url = elem.xpath("@src").extract_first()
        #    yield {'image_urls': [img_url]}

        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        for elem in response.xpath("//img"):
            img_url = elem.xpath("@src").extract_first()
            l.add_value('image_urls', [img_url])
            l.add_value('url', response.url)
            l.add_value('project', self.settings.get('BOT_NAME'))
            l.add_value('spider', self.name)
            l.add_value('server', socket.gethostname())
#            l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            yield l.load_item()