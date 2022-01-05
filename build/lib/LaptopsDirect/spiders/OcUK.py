# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider, Rule
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
from scrapy.linkextractors import LinkExtractor


class OcukSpider(SitemapSpider):
    name = 'OcUK'
    allowed_domains = ['overclockers.co.uk']
    sitemap_urls = ['https://www.overclockers.co.uk/cksitemaps/sitemap_products-1.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-2.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-3.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-4.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-5.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-6.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-7.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-8.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-9.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-10.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-11.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-12.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-13.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-14.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-15.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-16.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-17.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-18.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-19.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-20.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-21.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-22.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-23.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-24.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-25.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-26.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-27.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-28.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-29.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-30.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-31.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-32.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-33.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-34.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-35.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-36.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-37.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-38.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-39.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-40.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-41.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-42.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-43.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-44.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-45.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-46.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-47.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-48.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-49.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-50.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-51.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-52.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-53.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-54.xml',
    'https://www.overclockers.co.uk/cksitemaps/sitemap_products-55.xml',
    ]

    rules = (
        Rule(LinkExtractor(allow=()),callback='parse_item',follow=True),
#        Rule(LinkExtractor(allow=(),deny=(r'((?!\/archive).)*$', r'((?!\/b-grade-).)*$'))),
        Rule(LinkExtractor(allow=(),deny=(r'^https:\/\/www\.overclockers\.co\.uk\/archive(.*?)',
        r'^https:\/\/www\.overclockers\.co\.uk\/b-grade-(.*?)',
        r'^https:\/\/overclockers\.co\.uk\/archive(.*?)',
        r'^https:\/\/overclockers\.co\.uk\/b-grade-(.*?),',
        r'^https:\/\/overclockers\.co\.uk\/forums(.*?),',
        r'^https:\/\/www\.overclockers\.co\.uk\/forums(.*?)'))),
    )

    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        l.add_xpath('sku', '//*[@id="detail_bottom"]/p[3]/text()')
        l.add_xpath('price', '//*[@id="buy-wrapper"]/div[1]/div/strong/text()')
        l.add_xpath('product_title', '//*[@id="detailbox"]/div/div[2]/h1/text()')
        l.add_xpath('image_url', '//*[@id="zoom1"]/img')
        l.add_xpath('stock', '//*[@id="buybox"]/span/p/text()')
 
        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()