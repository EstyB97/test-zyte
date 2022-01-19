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

    #Kitchen range
        #Cookers
        #AEG
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Competence\s)(.*)(?=\sBuilt)")
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Competence\s)(.*)(?=\s{1,2}[0-9])")
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=AEG\s)(.*)(?=\sBuilt)")
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=AEG\s)(.*)(?=\s{1,2}[0-9])")
        #Baumatic
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Baumatic\s)(.*)(?=\s{1,2}[0-9])")
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Baumatic\s)(.*)(?=\sBuilt)")
        #benko
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Beko\s)(.*)(?=\s{1,2}[0-9])")
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Baumatic\s)(.*)(?=\sTelescopic)")
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Baumatic\s)(.*)(?=\sBuilt)")
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=RecycledNet.\s)(.*)(?=\sBuilt)")
        #Bosch
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Serie\s[0-9]\s)(.*)(?=\s{1,2}[0-9])")
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Serie\s[0-9]\s)(.*)(?=\sBuilt)")
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Bosch\s)(.*)(?=\sBuilt)")
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Bosch\s)(.*)(?=\sWifi)")
        #Candy
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Candy\s[0-9]\s)(.*)(?=\s{1,2}[0-9])")
        #Elica
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Elica\s[0-9]\s)(.*)(?=\s{1,2}[0-9])")
        #Hisense
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Hisense\s[0-9]\s)(.*)(?=\s{1,2}[0-9])")
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Hisense\s[0-9]\s)(.*)(?=\sBuilt)")
        #Hoover
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=CERAMIC\s)(.*)(?=\s{1,2}[0-9])")
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=[0-9]\s)(.*)(?=\s{1,2}[0-9])")
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=[0-9]\s)(.*)(?=\sBuilt)")
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=GAS\s)(.*)(?=\s{1,2}[0-9])")
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=INDUCTION\s)(.*)(?=\s{1,2}[0-9])")
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Hoover\s)(.*)(?=\s{1,2}[0-9])")
        #Hotpoint
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Hotpoint\s)(.*)(?=\s{1,2}[0-9])")
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Hotpoint\s)(.*)(?=\sBuilt)")
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Hotpoint\s)(.*)(?=\sMicrowave)")
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Class\s[0-9]\s)(.*)(?=\sBuilt)")
        #Indesit
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Indesit\s)(.*)(?=\s{1,2}[0-9])")
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Aria\s)(.*)(?=\sBuilt)")
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Indesit\s)(.*)(?=\sCooker)")
        #Leisure
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=[0-9]\s)(.*)(?=\s{1,2}[0-9])")
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Cookmaster\s)(.*)(?=\s{1,2}[0-9])")
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Leisure\s)(.*)(?=\s{1,2}[0-9])")
        #NEFF
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=[0-9]\s)(.*)(?=\s{1,2}[0-9])")
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Slide&Hide.\s)(.*)(?=\sBuilt)")
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=[0-9]\s)(.*)(?=\sWifi)")
        #Rangemaster
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Rangemaster\s)(.*)(?=\sRangecooker)")
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=PLUS\s)(.*)(?=\s{1,2}[0-9])")
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Toledo\s\+\s)(.*)(?=\s{1,2}[0-9])")
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Rangemaster\s)(.*)(?=\s{1,2}[0-9])")
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Esprit\s)(.*)(?=\s{1,2}[0-9])")
        #Samsung
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Samsung\s)(.*)(?=\sAmerican)")
        #Zanussi
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Zanussi\s)(.*)(?=\sBuilt)")
        

        #Fridge freezer
        #AEG
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=AEG\s)(.*)(?=\sIntegrated)")  
        #Beko
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Beko\s)(.*)(?=\sIntegrated)") 
        #Bosch
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Serie\s[0-9]\s)(.*)(?=\sIntegrated)") 
        #Candy 
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Candy\s)(.*)(?=\sBuilt)")    
        #Hisense 
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Hisense\s)(.*)(?=\sIntegrated)")
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Hisense\s)(.*)(?=\sAmerican)")
        #Hoover 
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Hoover\s)(.*)(?=\sBuilt)")
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Hoover\s)(.*)(?=\sIntegrated)")
        #Hotpoint 
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Hotpoint\s)(.*)(?=\sIntegrated)")
        #Indesit
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Indesit\s)(.*)(?=\sIntegrated)")
        #Neff 
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=NEFF\s)(.*)(?=\sIntegrated)")
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=[0-9]\s)(.*)(?=\sE)")
        #Samsung 
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=[0-9]\s)(.*)(?=\sAmerican)")
        #Smeg 
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Smeg\s)(.*)(?=\{1,2}[0-9])")


        #Dishwasher
        #AEG
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=AEG\s)(.*)(?=\Fully)") 
        #Beko
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Beko\s)(.*)(?=\Fully)") 
        #Bosch 
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Serie\s[0-9]\s)(.*)(?=\sFully)")
        #Candy 
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Candy\s)(.*)(?=\sWifi)")
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Candy\s)(.*)(?=\sSlimline)")
        #Hisense
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Hisense\s)(.*)(?=\sFully)")
        #Hoover
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Hoover\s)(.*)(?=\sFully)")
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=[0-9]\s)(.*)(?=\sWifi)")
        #Hotpoint
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Hotpoint\s)(.*)(?=\sFully)")
        #Indesit
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Indesit\s)(.*)(?=\sFully)")
        #Neff
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=[0-9]\s)(.*)(?=\sFully)")


        #Laundry
        #AEG
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=AEG\s)(.*)(?=\sIntegrated)")
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Technology\s)(.*)(?=\sIntegrated)") 
        #Beko 
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Beko\s)(.*)(?=\sIntegrated)")
        #Bosch 
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Serie\s[0-9]\s)(.*)(?=\sIntegrated)")
        #Candy 
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Candy\s)(.*)(?=\sWifi)")
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Rapido\s)(.*)(?=\sWifi)")
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=pro\s)(.*)(?=\sWifi)")
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Ultra\s)(.*)(?=\s{1,2}[0-9]kg)")
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Candy\s)(.*)(?=\sIntegrated)")
        #Hoover 
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=LITE\s)(.*)(?=\sintegrated)")
        #Hotpoint 
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Hotpoint\s)(.*)(?=\sIntegrated)")
        #Indesit 
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Indesit\s)(.*)(?=\sIntegrated)")
        #Neff 
        BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=NEFF\s)(.*)(?=\sIntegrated)")

        BB.add_value('url', response.url)
        BB.add_value('project', self.settings.get('BOT_NAME'))
        BB.add_value('useragent', self.settings.get('USER_AGENT'))
        BB.add_value('spider', self.name)
        BB.add_value('server', socket.gethostname())
        BB.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return BB.load_item()

        