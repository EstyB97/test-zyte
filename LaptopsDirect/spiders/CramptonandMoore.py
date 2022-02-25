from datetime import datetime
import socket
from scrapy.spiders import SitemapSpider #, Rule
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
from scrapy.linkextractors import LinkExtractor

class CramptonandMooreSpider(SitemapSpider):
    name = 'CramptonandMoore'
    custom_settings = { 
      'CLOSESPIDER_ERRORCOUNT': '500',
   }

    allowed_domains = ['cramptonandmoore.co.uk']
    sitemap_urls = ['https://www.cramptonandmoore.co.uk/sitemap.xml']

   
    def parse(self, response):
        AA = ItemLoader(item=LaptopsdirectItem(), response=response)

        AA.add_xpath('title','//meta[@itemprop="name"]/@content') # puling from meta tag
        AA.add_xpath('sku','//meta[@itemprop="sku"]/@content') # puling from meta tag 
        AA.add_xpath('price','//meta[@itemprop="price"]/@content') # puling from meta tag
        AA.add_xpath('stock','//div[@class="availability only"]/@title') # pulls how many is left in stock
        AA.add_xpath('stock','//div[@class="stock available"]//span[starts-with(.,"Availability")]//following::span[1]/text()') # states "in stock" if cant pull amount
        AA.add_xpath('stock','//div[@class="stock unavailable"]//span[starts-with(.,"Availability")]//following::span[1]/text()') # OOS capture 
        
        #STOVES SPESIFIC
        AA.add_xpath('sku','//span[starts-with(.,"Stoves")]/text()', re=r'(?<=Stoves\s[0-9]{9}\s)(.*?)(?=\s[0-9]{2})') 
        AA.add_xpath('sku','//span[starts-with(.,"Stoves")]/text()', re=r'(?<=Stoves\s)(.*?)(?=\s[0-9]{9}\s38L\s45cm)')
        AA.add_xpath('sku','//span[starts-with(.,"Stoves")]/text()', re=r'(?<=Deluxe\s)(.*?)(?=\s[0-9]{9}\s)')
        AA.add_xpath('sku','//span[starts-with(.,"Stoves")]/text()', re=r'(?<=ST\s[0-9]{9}\s)(.*?)(?=\sBlack)')
        AA.add_xpath('sku','//span[starts-with(.,"Stoves")]/text()', re=r'(?<=[0-9]{9}\s[0-9]{2}cm\s)(.*?)(?=\sDuel\sFuel)')

        #LEC SPESIFIC
        AA.add_xpath('sku','//span[starts-with(.,"Lec")]/text()', re=r'(?<=Lec\s[0-9]{9}\s)(.*?)(?=\s)')
        AA.add_xpath('sku','//span[starts-with(.,"Lec")]/text()', re=r'(?<=Lec\s)(.*?)(?=\s\d\d)')
        AA.add_xpath('sku','//span[starts-with(.,"Lec")]/text()', re=r'(?<=Lec\s)(.*?)(?=\s[0-9]{9})')

        #BRITANNIA SPESIFIC
        AA.add_xpath('sku','//span[starts-with(.,"Britannia")]/text()', re=r'(?<=Q\-Line\s)(.*?)(?=\s\d)')

        #BELLING
        AA.add_xpath('sku','//span[starts-with(.,"Belling")]/text()', re=r'(?<=Belling\s)(.*?)(?=\s[0-9]{9}\s72L)')




        
        
        
        
        
        
        
        
        
        
        
        AA.add_value('url', response.url)
        #AA.add_value('Project', self.settings.get('BOT_NAME'))
        AA.add_value('useragent', self.settings.get('USER_AGENT'))
        AA.add_value('spider', self.name)
        AA.add_value('server', socket.gethostname())
        AA.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return AA.load_item()
