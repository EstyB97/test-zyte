from scrapy.spiders import CrawlSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem

class BbqWorldSpider(CrawlSpider):
    name = 'BbqWorld'

    allowed_domains = ['bbqworld.co.uk']
    start_urls = ['https://www.bbqworld.co.uk/weber-barbecues/weberq/weber-q1200-black-with-stand.asp']

    def parse_item(self, response):
        BB = ItemLoader(item=LaptopsdirectItem(), response=response)

        BB.add_xpath ('title','//tbody//h1/text()')
        BB.add_xpath ('sku','//p//span[@itemprop="sku"]/text()')
        BB.add_xpath ('price','//span[@itemprop="price"]/text()')
        BB.add_xpath ('stock','//tbody//tr//td[@class="BorderTopLine"]//strong/text()')

        return BB.load_item()
        