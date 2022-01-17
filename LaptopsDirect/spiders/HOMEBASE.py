from datetime import datetime
from scrapy.spiders import SitemapSpider, Rule
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
#from scrapy.linkextractors import LinkExtractor
import socket

class HOMEBASESpider(SitemapSpider):
    name = 'HOMEBASE'
    custom_settings = { 
      'DOWNLOAD_DELAY': '0.08', 
      'AUTOTHROTTLE_START_DELAY': '4',
      'AUTOTHROTTLE_MAX_DELAY': '80', 
      'AUTOTHROTTLE_TARGET_CONCURRENCY': '16', 
      'CLOSESPIDER_ERRORCOUNT': '500',
      'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362',
      'CONCURRENT_REQUESTS': '24', 
      'ROBOTSTXT_OBEY': 'False',
   }
   #custom_settings = { 
        #'DOWNLOADER_MIDDLEWARES' : {
            #'LaptopsDirect.middlewares.CustomProxyMiddleware': 350,
            #'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 400,
            #'LaptopsDirect.middlewares.RotatingProxyMiddleware': 610,
            #'LaptopsDirect.middlewares.BanDetectionMiddleware': 620,
        #},
        #'CLOSESPIDER_TIMEOUT' : '864000'
    #}


    allowed_domains = ['homebase.co.uk']
    sitemap_urls = ['https://www.homebase.co.uk/sitemap-product-0.xml.gz']


    def parse(self, response):
        BB = ItemLoader(item=LaptopsdirectItem(), response=response)

        BB.add_xpath ('title','//h1[@class="productName_title"]/text()')
        BB.add_xpath ('sku','//div[@id="product-description-content-lg-9"]//div[@data-information-component="hbg_modelNumber"]/div/text()')
        BB.add_xpath ('sku','//div[@class="externalSku"]/text()')
        BB.add_xpath ('price','//p[@data-product-price="price"]/text()', re=r"(.+)")
        BB.add_xpath ('stock','//p[@class="productStockInformation_prefix"]/text()')

        BB.add_value('url', response.url)
        BB.add_value('project', self.settings.get('BOT_NAME'))
        BB.add_value('useragent', self.settings.get('USER_AGENT'))
        BB.add_value('spider', self.name)
        BB.add_value('server', socket.gethostname())
        BB.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return BB.load_item()

        