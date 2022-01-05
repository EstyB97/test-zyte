from datetime import datetime
import urlparse
#import urllib.parse
import socket
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem


class ArgosSpider(SitemapSpider):
    name = 'Argos'
    custom_settings = { 
        'DOWNLOADER_MIDDLEWARES' : {
            'LaptopsDirect.middlewares.CustomProxyMiddleware': 350,
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 400,
        },
   }
    allowed_domains = ['argos.co.uk']
    sitemap_urls = ['https://www.argos.co.uk/product.xml', 'https://www.argos.co.uk/product2.xml']

    def parse(self, response):
        l = ItemLoader(item=LaptopsdirectItem(), response=response)

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')
        l.add_xpath('product_title', '//span[@data-test="product-title"]/text()')

        #Individual SKU handling
        l.add_xpath('sku', '//span[starts-with(.,"Hoover H-HOB 500")]', re=r"(?<=Hoover H-HOB 500)(.*)(?=Bridge Ceramic Hob)")
        l.add_xpath('sku', '//span[starts-with(.,"Hoover H-OVEN 300")]', re=r"(?<=Hoover H-OVEN 300)(.*)(?=Built In Single Oven)")
        l.add_xpath('sku', '//span[starts-with(.,"Hoover H-HOOD 300")]', re=r"(?<=Hoover H-HOOD 300)(.*)(?=Cooker Hood)")
        l.add_xpath('sku', '//span[starts-with(.,"Hoover H-HOB 300")]', re=r"(?<=Hoover H-HOB 300)(.*)(?=Induction Hob)")
        

        l.add_xpath('sku', '//*[@id="content"]//table/tbody/tr//th[starts-with(.,"Model number")]/following::td[1]/text()')
        l.add_xpath('sku', '//*[@id="product-description"]/div/p[starts-with(.,"Model number:")]/text()')
        l.add_xpath('sku', '//div[@itemprop="description"]/p[starts-with(.,"Model number:")]/text()')
        l.add_xpath('sku', '//div[@itemprop="description"]//li[starts-with(.,"Model number:")]/text()')
        #Take the second word out of the title as a catch-all for SKUs
        l.add_xpath('sku', '//span[@data-test="product-title"]/text()', re=r"^(?:[^\s]*\s){1}([^\s]*)")
        #l.add_xpath('sku', 'substring-after(//span[@data-test="product-title"]/text(),' ')')
        l.add_xpath('price', '//li[@itemprop="price"]/@content')
        l.add_xpath('stock', '//*[@id="add-to-trolley-quantity"]/option/@value')
        l.add_xpath('pcwb_product_code', '//span[@itemprop="sku"]/@content')

        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()