from datetime import datetime
import socket
from scrapy.spiders import SitemapSpider #, Rule
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
#from scrapy.linkextractors import LinkExtractor

class APLICSpider(SitemapSpider):
    name = 'APLIC'
    custom_settings = { 
      'CLOSESPIDER_ERRORCOUNT': '500',
   }

    allowed_domains = ['appliancecity.co.uk']
    sitemap_urls = ['https://www.appliancecity.co.uk/product-sitemap1.xml', 
    'https://www.appliancecity.co.uk/product-sitemap1.xml', 
    'https://www.appliancecity.co.uk/product-sitemap2.xml', 
    'https://www.appliancecity.co.uk/product-sitemap3.xml',
    'https://www.appliancecity.co.uk/product-sitemap4.xml',
    'https://www.appliancecity.co.uk/product-sitemap5.xml',
    'https://www.appliancecity.co.uk/product-sitemap6.xml',
    'https://www.appliancecity.co.uk/product-sitemap7.xml',
    'https://www.appliancecity.co.uk/product-sitemap8.xml',
    'https://www.appliancecity.co.uk/product-sitemap9.xml',
    'https://www.appliancecity.co.uk/product-sitemap10.xml',
    'https://www.appliancecity.co.uk/product-sitemap11.xml',]

    #rules = (
     # Rule(LinkExtractor(allow=(),deny=(r'')),callback='parse_item',follow=True),
    #)

    def parse(self, response):
        AA = ItemLoader(item=LaptopsdirectItem(), response=response)

        AA.add_xpath('url','//head//script[@type="text/javascript"][1]/@src')
        AA.add_xpath('title','/html/head/title/text()')
        AA.add_xpath('sku','//div[@class="acity-product-trustpilot-widget acity-product-single-trustpilot-widget trustpilot-widget"]/@data-sku')
        AA.add_xpath('price','//h1/following::p[1]/span/bdi/text()')
        AA.add_xpath('price','//div[@class="single-product-infos"]/div/p/span/text()')
        AA.add_xpath('price','//p[@class="price"]/span[@class="woocommerce-Price-amount amount"]/text()')
        AA.add_xpath('stock','//div[@class="acity-product-availability acity-product-availability-in-stock acity-product-single-availability"]/text()')
        AA.add_xpath('stock','//p[@class="price"]/following::div[1]/text()')
        AA.add_xpath('stock','//p[@class="acity-product-strapline acity-product-single-strapline"]/text()')

        AA.add_value('url', response.url)
        #AA.add_value('Project', self.settings.get('BOT_NAME'))
        AA.add_value('useragent', self.settings.get('USER_AGENT'))
        AA.add_value('spider', self.name)
        AA.add_value('server', socket.gethostname())
        AA.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return AA.load_item()
