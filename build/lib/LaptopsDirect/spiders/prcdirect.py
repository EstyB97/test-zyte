from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem


class PrcDirectSpider(SitemapSpider):
    name = 'prcdirect'
    custom_settings = { 
      'ROBOTSTXT_OBEY': 'False', 
    }
    allowed_domains = ['prcdirect.co.uk']
    sitemap_urls = ['https://prcdirect.co.uk/sitemap.xml']

    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '//*[@id="Head"]/title/text()')
        l.add_xpath('sku', '//div[@class="sku"]/span[@class="value"]/text()')
        l.add_xpath('price', '/html/head/meta[@property="og:price:amount"]/@content')
        l.add_xpath('stock', '/html/head/meta[@property="og:availability"]/@content')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()