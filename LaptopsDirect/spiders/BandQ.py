from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
import socket
from datetime import datetime


class BandQSpider(SitemapSpider):
    name = 'BandQ'

    
    allowed_domains = ['diy.com']
    sitemap_urls = ['https://www.diy.com/static/sitemap.xml']

    def parse(self, response):
        BB = ItemLoader(item=LaptopsdirectItem(), response=response)

        BB.add_xpath ('title','//h1[@data-test-id="hero-info-title"]/text()')
        BB.add_xpath ('sku','//td[@data-test-id="product-ean-spec"]/text()')
        BB.add_xpath ('price','//section//div[@data-test-id="product-primary-price"]//span//text()')
        BB.add_xpath ('stock','//input[@name="quantity"]/@value')

        
         # Administration Fields
        BB.add_value('url', response.url)
        BB.add_value('project', self.settings.get('BOT_NAME'))
        BB.add_value('useragent', self.settings.get('USER_AGENT'))
        BB.add_value('spider', self.name)
        BB.add_value('server', socket.gethostname())
        BB.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


        return BB.load_item() 
        