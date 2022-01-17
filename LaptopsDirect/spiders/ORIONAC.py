from scrapy.spiders import SitemapSpider, Rule
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
from scrapy.linkextractors import LinkExtractor
class ORIONACSpider(SitemapSpider):
    name = 'ORIONAC'

    allowed_domains = ['orionairsales.co.uk']
    sitemap_urls = ['http://www.orionairsales.co.uk/sitemap.xml']

    rules = (
        Rule(LinkExtractor(allow=()),callback='parse_item',follow=True),
#        Rule(LinkExtractor(allow=(),deny=(r'((?!\/archive).)*$', r'((?!\/b-grade-).)*$'))),
        Rule(LinkExtractor(allow=(),deny=(r'^https:\/\/www\.orionairsales\.co\.uk\/terms\.asp(.*?)',
        r'^https:\/\/www\.orionairsales\.co\.uk\/company-news-33-w\.asp(.*?)',
        r'^https:\/\/www\.orionairsales\.co\.uk\/refrigeration-compressors-34-w\.asp(.*?)',
        r'^https:\/\/www\.orionairsales\.co\.uk\/about-us-1-w\.asp(.*?)',
        r'^https:\/\/orionairsales\.co\.uk\/contact-us-2-w\.asp(.*?)',
        r'^https:\/\/orionairsales\.co\.uk\/air-con-info-3-w\.asp(.*?),',
        r'^https:\/\/orionairsales\.co\.uk\/air-heat-pumps-explained-12-w\.asp(.*?),',
        r'^https:\/\/www\.orionairsales\.co\.uk\/which-space-heater-15-w\.asp(.*?)'))),
    )

    def parse(self, response):
        BB = ItemLoader(item=LaptopsdirectItem(), response=response)

        BB.add_xpath ('title','//span[@class="breadcrumbs-product"]/text()')
        BB.add_xpath ('sku','//script[@type="application/ld+json"]', re=r"(mpn\":\")(.*?)(?=\")")
        BB.add_xpath ('price','//span[@itemprop="price"]/text()')
        BB.add_xpath ('stock','//span[@id="_EKM_PRODUCTSTOCK"]//span/text()')

        return BB.load_item()