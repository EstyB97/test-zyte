from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
import socket
from datetime import datetime

class OrionAirSalesSpider(SitemapSpider):
    name = 'OrionAirSales'

    allowed_domains = ['orionairsales.co.uk']
    sitemap_urls = ['http://www.orionairsales.co.uk/sitemap.xml']

    def parse(self, response):
        BB = ItemLoader(item=LaptopsdirectItem(), response=response)

        BB.add_xpath ('title','//span[@class="breadcrumbs-product"]/text()')
        BB.add_xpath ('sku','//span[@class="breadcrumbs-product"]/text()')
        BB.add_xpath ('price','//span[@itemprop="price"]/text()')
        BB.add_xpath ('stock','//span[@id="_EKM_PRODUCTSTOCK"]//span/text()')

        # Administration Fields
        BB.add_value('url', response.url)
        BB.add_value('project', self.settings.get('BOT_NAME'))
        BB.add_value('useragent', self.settings.get('USER_AGENT'))
        BB.add_value('spider', self.name)
        BB.add_value('server', socket.gethostname())
        BB.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return BB.load_item()