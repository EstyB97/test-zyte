from datetime import datetime
from scrapy.spiders import SitemapSpider, Rule
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
#from scrapy.linkextractors import LinkExtractor
import socket

class ORIONACSpider(SitemapSpider):
    name = 'ORIONAC'

    allowed_domains = ['homebase.co.uk']
    sitemap_urls = ['https://www.homebase.co.uk/sitemapindex-product.xml.gz']


    def parse(self, response):
        BB = ItemLoader(item=LaptopsdirectItem(), response=response)

        BB.add_xpath ('title','//h1[@class="productName_title"]/text()')
        BB.add_xpath ('sku','//div[@id="product-description-content-lg-9"]//div[@data-information-component="hbg_modelNumber"]/div/text()')
        BB.add_xpath ('sku','//div[@class="externalSku"]/text()')
        BB.add_xpath ('price','//p[@class="productPrice_price "]/text()')
        BB.add_xpath ('stock','//p[@class="productStockInformation_prefix"]/text()')

        BB.add_value('url', response.url)
        BB.add_value('project', self.settings.get('BOT_NAME'))
        BB.add_value('useragent', self.settings.get('USER_AGENT'))
        BB.add_value('spider', self.name)
        BB.add_value('server', socket.gethostname())
        BB.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return BB.load_item()