from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem

class BQSSpider(SitemapSpider):
    name = "BQS"


    allowed_domains = ['thebbqshop.co.uk']
    sitemap_urls = ['https://thebbqshop.co.uk/sitemap.xml']

    def parse(self, response):
        SS = ItemLoader(item=LaptopsdirectItem(), response=response)

        SS.add_xpath ('title','//div/h1/text()')
        SS.add_xpath ('sku','//li/font[@data-ro="product-model"]/text()')
        SS.add_xpath ('price','//div//h2/text()')
        SS.add_xpath ('stock','//li//font[@data-ro="product-stock"]/text()')

        return SS.load_item()
