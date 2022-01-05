from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem

class RDSpider(SitemapSpider):
    name = 'RD'

    allowed_domains = ['robertdyas.co.uk']
    sitemap_urls = ['https://www.robertdyas.co.uk/pub/media/sitemap/sitemap_001.xml', 'https://www.robertdyas.co.uk/pub/media/sitemap/sitemap_002.xml', 'https://www.robertdyas.co.uk/pub/media/sitemap/sitemap_003.xml', 'https://www.robertdyas.co.uk/pub/media/sitemap/sitemap_004.xml', 'https://www.robertdyas.co.uk/pub/media/sitemap/sitemap_005.xml', 'https://www.robertdyas.co.uk/media/bloom_reach_thematic_sitemap/sitemap_robertdyas_uk_main_en_gb_1.xml']

    def parse(self, response):
        BB = ItemLoader(item=LaptopsdirectItem(), response=response)

        BB.add_xpath ('title','//h1//span[@itemprop="name"]/text()')
        BB.add_xpath ('sku','//div[@class="product-attribute-value js-product-attribute-model"]/text()', re=r"(.+)")
        BB.add_xpath ('sku','//div[@class="product-attribute-value js-product-attribute-sku"]/text()', re=r"(.+)")
        BB.add_xpath ('price','//div[@class="price-box price-final_price"]//span[@class="price"]/text()')
        BB.add_xpath ('stock','//div[@class="stock available"]//span/text() | //div//p[@title="Availability"]//span/text()')

        
        return BB.load_item()

        