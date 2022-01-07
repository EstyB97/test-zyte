from datetime import datetime
import socket
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
from scrapy.linkextractors import LinkExtractor


class WAYFpider(CrawlSpider):
    name = 'WAYF'
    custom_settings = {
    'CLOSESPIDER_TIMEOUT':'864000',
    'CONCURRENT_REQUESTS':'2',
    'RETRY_TIMES':'5',
    'REDIRECT_ENABLED':'false'
    }

    allowed_domains = ['wayfair.co.uk']
    start_urls = ['https://www.wayfair.co.uk/']
    
    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//div[@class="premmerce-filter-ajax-container"]',
        '//div[@class="premmerce-filter-ajax-container"]',
        '//article[@class="CategoryCarousel"]')) 
        callback='parse_item', follow=True),
    )

    #def parse(self, response):
        #for link in response.css('a::attr(href)'):
            #yield response.follow(link.getall(), callback=self.parse_items)

    def parse_items(self, response):

        TT = ItemLoader(item=LaptopsdirectItem(), response=response)

        TT.add_xpath ('title','//div[@data-enzyme-id="TitleBlock"]//h1/text()')
        TT.add_xpath ('sku','//input[@type="hidden"][@name="sku"]/@value')
        TT.add_xpath ('price','//span[@class="pl-Box--mr-1 pl-Box--pr-1 pl-Price-V2 pl-Price-V2--5000 pl-Box--baseColor"]/text()')
        TT.add_xpath ('price','//span[@class="pl-Box--mr-1 pl-Box--pr-1 pl-Price-V2 pl-Price-V2--5000 pl-Box--saleColor"]/text()')
        TT.add_xpath ('stock','//span[@class="ShippingHeadline-text"]/text()')

        TT.add_value('url', response.url)
        TT.add_value('project', self.settings.get('BOT_NAME'))
        TT.add_value('useragent', self.settings.get('USER_AGENT'))
        TT.add_value('spider', self.name)
        TT.add_value('server', socket.gethostname())
        TT.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return TT.load_item() 
        