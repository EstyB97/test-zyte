from datetime import datetime
from scrapy.spiders import SitemapSpider, Rule
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
from scrapy.linkextractors import LinkExtractor
import socket

class CramptonandMooreSpider(SitemapSpider):
    name = 'CramptonandMoore'
    
    allowed_domains = ['cramptonandmoore.co.uk']
    sitemap_urls = ['https://www.cramptonandmoore.co.uk/sitemap.xml']
    


    def parse(self, response):
        BB = ItemLoader(item=LaptopsdirectItem(), response=response)

        BB.add_xpath('title','//meta[@itemprop="name"]/@content') # puling from meta tag
        BB.add_xpath('sku','//meta[@itemprop="sku"]/@content') # puling from meta tag 
        BB.add_xpath('price','//meta[@itemprop="price"]/@content') # puling from meta tag
        BB.add_xpath('stock','//div[@class="availability only"]/@title') # pulls how many is left in stock
        BB.add_xpath('stock','//div[@class="stock available"]//span[starts-with(.,"Availability")]//following::span[1]/text()') # states "in stock" if cant pull amount
        BB.add_xpath('stock','//div[@class="stock unavailable"]//span[starts-with(.,"Availability")]//following::span[1]/text()') # OOS capture 
        
        #STOVES SPESIFIC
        BB.add_xpath('sku','//span[starts-with(.,"Stoves")]/text()', re=r'(?<=Stoves\s[0-9]{9}\s)(.*?)(?=\s[0-9]{2})') 
        BB.add_xpath('sku','//span[starts-with(.,"Stoves")]/text()', re=r'(?<=Stoves\s)(.*?)(?=\s[0-9]{9}\s38L\s45cm)')
        BB.add_xpath('sku','//span[starts-with(.,"Stoves")]/text()', re=r'(?<=Deluxe\s)(.*?)(?=\s[0-9]{9}\s)')
        BB.add_xpath('sku','//span[starts-with(.,"Stoves")]/text()', re=r'(?<=ST\s[0-9]{9}\s)(.*?)(?=\sBlack)')
        BB.add_xpath('sku','//span[starts-with(.,"Stoves")]/text()', re=r'(?<=[0-9]{9}\s[0-9]{2}cm\s)(.*?)(?=\sDuel\sFuel)')

        #LEC SPESIFIC
        BB.add_xpath('sku','//span[starts-with(.,"Lec")]/text()', re=r'(?<=Lec\s[0-9]{9}\s)(.*?)(?=\s)')
        BB.add_xpath('sku','//span[starts-with(.,"Lec")]/text()', re=r'(?<=Lec\s)(.*?)(?=\s\d\d)')
        BB.add_xpath('sku','//span[starts-with(.,"Lec")]/text()', re=r'(?<=Lec\s)(.*?)(?=\s[0-9]{9})')

        #BRITANNIA SPESIFIC
        BB.add_xpath('sku','//span[starts-with(.,"Britannia")]/text()', re=r'(?<=Q\-Line\s)(.*?)(?=\s\d)')

        #BELLING
        BB.add_xpath('sku','//span[starts-with(.,"Belling")]/text()', re=r'(?<=Belling\s)(.*?)(?=\s[0-9]{9}\s72L)')


       
         # Administration Fiels
        BB.add_value('url', response.url)
        BB.add_value('project', self.settings.get('BOT_NAME'))
        BB.add_value('useragent', self.settings.get('USER_AGENT'))
        BB.add_value('spider', self.name)
        BB.add_value('server', socket.gethostname())
        BB.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return BB.load_item()

        