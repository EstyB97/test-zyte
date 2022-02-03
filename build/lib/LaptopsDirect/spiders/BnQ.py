from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem

class BnQSpider(SitemapSpider):
    name = 'BnQ'

    
    allowed_domains = ['diy.com']
    sitemap_urls = ['https://www.diy.com/static/sitemap.xml']

    def parse(self, response):
        TT = ItemLoader(item=LaptopsdirectItem(), response=response)

        TT.add_xpath ('title','//h1[@data-test-id="hero-info-title"]/text()')
        TT.add_xpath ('sku','//tbody//th[starts-with(.,"Model name/number")]/following::td[1]/text()') # Model name/number
        TT.add_xpath ('sku2','//tbody//th[starts-with(.,"Product code")]/following::td[1]/text()') # Product code 
        TT.add_xpath ('price','//section//div[@data-test-id="product-primary-price"]//span//text()')
        TT.add_xpath ('stock','//input[@name="quantity"]/@value')


        return TT.load_item() 
        