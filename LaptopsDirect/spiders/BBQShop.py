from scrapy.spiders import SitemapSpider, Rule
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
import socket
from datetime import datetime
from scrapy.linkextractors import LinkExtractor

class BBQShopSpider(SitemapSpider):
    name = "BBQShop"


    allowed_domains = ['thebbqshop.co.uk']
    sitemap_urls = ['https://thebbqshop.co.uk/sitemap.xml']
    #sitemap_rules = [
       # ('/bbq-spares/', 'parse_nothing', '/', 'parse')
    #]
    rules = (
        Rule(LinkExtractor(allow=()),callback='parse',follow=True),
        Rule(LinkExtractor(allow=(r'https?://thebbqshop.co.uk/bbq-accessories/.*',
         r'https?://thebbqshop.co.uk/BBQs/.*',
         r'https?://thebbqshop.co.uk/Gas%20BBQ%20Fittings/.*',
         r'https?://calor-gas-heaters/.*',
         r'https?://thebbqshop.co.uk/fuels/.*',
         r'https?://thebbqshop.co.uk/.*',),
         
        deny=(r'^https?://thebbqshop.co.uk/bbq-spares/spares-by-brand/.*',
        
        ))),
    )
   

    def parse(self, response):
        BB = ItemLoader(item=LaptopsdirectItem(), response=response)
    
        BB.add_xpath ('title','//div/h1/text()')
        BB.add_xpath ('sku','//li/font[@data-ro="product-model"]/text()')
        BB.add_xpath ('price','//div//h2/text()')
        BB.add_xpath ('stock','//li//font[@data-ro="product-stock"]/text()')

         # Administration Fields
        BB.add_value('url', response.url)
        BB.add_value('project', self.settings.get('BOT_NAME'))
        BB.add_value('useragent', self.settings.get('USER_AGENT'))
        BB.add_value('spider', self.name)
        BB.add_value('server', socket.gethostname())
        BB.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        return BB.load_item()
    
    def parse_nothing(self, response):
        TT = ItemLoader(item=LaptopsdirectItem(), response=response)

        return TT.load_item()
        
