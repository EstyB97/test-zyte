from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
import socket
from datetime import datetime


class AirConditioningWorldSpider(SitemapSpider):
    name = 'AirConditioningWorld'

    allowed_domains = ['airconditioningworld.co.uk']
    sitemap_urls = ['https://www.airconditioningworld.co.uk/sitemap.xml']

    def parse(self, response):
        BB = ItemLoader(item=LaptopsdirectItem(), response=response)

        BB.add_xpath ('title','//div[@id="product-main-info"]/h1/text()')
        BB.add_xpath ('sku','//div[@id="product-main-info"]/h1/text()', re=r"(?<=Haier\s)(.*)(?=[-|\s][0-9]{1,2}.[0-9][A-Za-z])")
        BB.add_xpath ('sku','//div[@id="product-main-info"]/h1/text()', re=r"(?<=Carrier)(.*)(?=[-|\s][0-9]{1,2}.[0-9][A-Za-z])")
        BB.add_xpath ('sku','//div[@id="product-main-info"]/h1/text()', re=r"(?<=Midea)(.*)(?=[-|\s][0-9]{1,2}.[0-9][A-Za-z])")
        BB.add_xpath ('sku','//div[@id="product-main-info"]/h1/text()', re=r"(?<=Industries)(.*)(?=[-|\s][0-9]{1,2}.[0-9][A-Za-z])")
        BB.add_xpath ('sku','//div[@id="product-main-info"]/h1/text()', re=r"(?<=Electric)(.*)(?=[-|\s][0-9]{1,2}.[0-9][A-Za-z])")
        BB.add_xpath ('sku','//div[@id="product-main-info"]/h1/text()', re=r"(?<=Toshiba)(.*)(?=[-|\s][0-9]{1,2}.[0-9][A-Za-z])")
        BB.add_xpath ('sku','//div[@id="product-main-info"]/h1/text()', re=r"(?<=LG)(.*)(?=[-|\s][0-9]{1,2}.[0-9][A-Za-z])")
        BB.add_xpath ('sku','//div[@id="product-main-info"]/h1/text()', re=r"(?<=Samsung)(.*)(?=[-|\s][0-9]{1,2}.[0-9][A-Za-z])")
        BB.add_xpath ('sku','//div[@id="product-main-info"]/h1/text()', re=r"(?<=Fujitsu)(.*)(?=[-|\s][0-9]{1,2}.[0-9][A-Za-z])")
        BB.add_xpath ('sku','//div[@id="product-main-info"]/h1/text()', re=r"(?<=Hitachi\s)(.*)(?=[-|\s][0-9]{1,2}.[0-9][A-Za-z])")
        BB.add_xpath ('sku','//div[@id="product-main-info"]/h1/text()', re=r"(?<=Module\s)(.*)")
        BB.add_xpath ('sku','//div[@id="product-main-info"]/h1/text()', re=r"(?<=Daikin\s)(.*)(?=\sBlack)")
        BB.add_xpath ('sku','//div[@id="product-main-info"]/h1/text()', re=r"(?<=Daikin\s)(.*)(?=\sSilver)")
        BB.add_xpath ('sku','//div[@id="product-main-info"]/h1/text()', re=r"(?<=Daikin\s)(.*)(?=\sWhite)")
        BB.add_xpath ('sku','//div[@id="product-main-info"]/h1/text()', re=r"(?<=Daikin\s)(.*)(?=[-|\s][0-9]{1,2}.[0-9][A-Za-z])")
        BB.add_xpath ('sku','//div[@id="product-main-info"]/h1/text()', re=r"(?<=Panasonic\s)(.*)(?=[-|\s][0-9]{1,2}.[0-9][A-Za-z])")
        BB.add_xpath ('sku','//div[@id="product-main-info"]/h1/text()', re=r"(?<=Sinclair\s)(.*)(?=[-|\s][0-9]{1,2}.[0-9][A-Za-z])")
        BB.add_xpath ('price','//div[@id="product-price"]/text()[1]|//span[@class="smaller"]/text()')
        BB.add_xpath ('stock','//label/input[@name="quantity"]/@value')
        BB.add_xpath ('url', '//form[@action="/processform"]/input/@value')
        
         # Administration Fields
        BB.add_value('url', response.url)
        BB.add_value('project', self.settings.get('BOT_NAME'))
        BB.add_value('useragent', self.settings.get('USER_AGENT'))
        BB.add_value('spider', self.name)
        BB.add_value('server', socket.gethostname())
        BB.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return BB.load_item()

        