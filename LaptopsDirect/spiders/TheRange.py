from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
import socket
from datetime import datetime

class TheRangeSpider(SitemapSpider):
    name = "TheRange"
    headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
    'Sec-Fetch-User': '?1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    }

    allowed_domains = ['therange.co.uk']
    sitemap_urls = ['https://www.therange.co.uk/sitemap/sitemap-1.xml', 'https://www.therange.co.uk/sitemap/sitemap-2.xml']

    def parse(self, response):
        BB = ItemLoader(item=LaptopsdirectItem(), response=response, headers=headers)

        BB.add_xpath ('title','//h1[@id="product-dyn-title"]/text()')
        BB.add_xpath ('sku','//span[@id="product-dyn-code"]/text()')
        BB.add_xpath ('price','//div[@id="min_price"]/text()')
        BB.add_xpath ('stock', '//span[@id="geo_prod_delivery_status"]/text()')

        # Administration Fields 
        BB.add_value('url', response.url)
        BB.add_value('project', self.settings.get('BOT_NAME'))
        BB.add_value('useragent', self.settings.get('USER_AGENT'))
        BB.add_value('spider', self.name)
        BB.add_value('server', socket.gethostname())
        BB.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))



        return BB.load_item()
