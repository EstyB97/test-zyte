# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
import socket
import scrapy
import re
from scrapy import selector
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
import logging
from scrapy.loader.processors import TakeFirst
from requests import get

ip = get('https://api.ipify.org').text
get('https://www.duckdns.org/update?domains=cabbage51&token=96e0eeee-e2f3-4788-a861-dfeac8b55126&ip='.format(ip))

#Custom downloader middleware uses a proxy to disguise where the request is coming from. Proxy has to be UK based or will only work for a couple of runs. Limited number of runs per proxy per day as there is some sort of
#counting in place on the number of page requests per IP. If a custom user agent is used they will block it automatically. Conditional based fields are listed below and Regex on the import into our data
#extracts out the first found node. Nodes in this spider return blank ([]) rather than NULL through the API due to the use of the re library for regex processing.

class TCSpider(SitemapSpider):
    name = 'TC'
    custom_settings = { 
        'DOWNLOADER_MIDDLEWARES' : {
            'LaptopsDirect.middlewares.CustomProxyMiddleware': 350,
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 400,
        },
        'CLOSESPIDER_TIMEOUT' : '864000'
   }
    allowed_domains = ['currys.co.uk']
    sitemap_urls = ['https://www.currys.co.uk/robots.txt']
    #handle_httpstatus_list = [301, 302, 200]
    
    def parse(self, response):

        l = ItemLoader(item=LaptopsdirectItem(), response=response)
        #l.default_output_processor = TakeFirst()   -- Breaks the JSON on integration

        l.add_xpath('//h1[@class="page-title nosp"]/span[2]/text()', re=r"")
            
        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()