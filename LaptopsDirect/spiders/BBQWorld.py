from datetime import datetime
from scrapy.spiders import SitemapSpider, Rule
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
from scrapy.linkextractors import LinkExtractor
import socket

class BBQWorldSpider(SitemapSpider):
    name = 'BBQWorld'
    
    allowed_domains = ['bbqworld.co.uk']
    sitemap_urls = ['http://www.bbqworld.co.uk/sitemap.xml']
    


    def parse(self, response):
        BB = ItemLoader(item=LaptopsdirectItem(), response=response)

        BB.add_xpath ('title','//tbody//h1/text()')
        BB.add_xpath ('sku','//p//span[@itemprop="sku"]/text()')
        BB.add_xpath ('price','//span[@itemprop="price"]/text()')
        BB.add_xpath ('stock','//tbody//tr//td[@class="BorderTopLine"]//strong/text()')

         # Administration Fiels
        BB.add_value('url', response.url)
        BB.add_value('project', self.settings.get('BOT_NAME'))
        BB.add_value('useragent', self.settings.get('USER_AGENT'))
        BB.add_value('spider', self.name)
        BB.add_value('server', socket.gethostname())
        BB.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return BB.load_item()
