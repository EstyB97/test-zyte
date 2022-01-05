from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem

class ORIONACSpider(SitemapSpider):
    name = 'ORIONAC'

    allowed_domains = ['orionairsales.co.uk']
    sitemap_urls = ['http://www.orionairsales.co.uk/sitemap.xml']

    def parse(self, response):
        BB = ItemLoader(item=LaptopsdirectItem(), response=response)

        BB.add_xpath ('title','//span[@class="breadcrumbs-product"]/text()')
        BB.add_xpath ('sku','//span[@class="breadcrumbs-product"]/text()')
        BB.add_xpath ('price','//span[@itemprop="price"]/text()')
        BB.add_xpath ('stock','//span[@id="_EKM_PRODUCTSTOCK"]//span/text()')

        return BB.load_item()