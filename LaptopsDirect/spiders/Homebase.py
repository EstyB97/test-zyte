from datetime import datetime
from scrapy.spiders import SitemapSpider, Rule
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
from scrapy.linkextractors import LinkExtractor
import socket

class HomebaseSpider(SitemapSpider):
    name = 'Homebase'
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
    #sitemap_rules = [('zanussi-zpvf4131x-built-in-electric-single-oven-and-ceramic-hob-pack-stainless-steel/13482044.html'),]

    #rules = [
        #Rule(LinkExtractor(allow=(r'https:\/\/www\.homebase\.co\.uk\/zanussi(.*)')),
        #callback='parse_item', follow=True),
    #]


    def parse(self, response):
        BB = ItemLoader(item=LaptopsdirectItem(), response=response)

        BB.add_xpath ('title','//h1[@class="productName_title"]/text()')
        #BB.add_xpath ('sku','//div[@id="product-description-content-lg-9"]//div[@data-information-component="hbg_modelNumber"]/div/text()')
        BB.add_xpath ('price','//p[@data-product-price="price"]/text()', re=r"(.+)")
        BB.add_xpath ('stock','//p[@class="productStockInformation_prefix"]/text()')
        BB.add_xpath ('sku2','/html/body/script[1]/text()', re=r'(?<=productSKU\'\:\')(.*?)(\')')
    
        #AEG
        if response.xpath ('//h1[@class="productName_title"]/text()[starts-with(.,"AEG")]'):
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Technology\s)(.*?)(?=\sIntegrated\s\d)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Technology\s)(.*?)(?=\sIntegrated\s\d\d)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=AEG\s)(.*?)(?=\sIntegrated\sFridge)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=AEG\s)(.*?)(?=\sIntegrated\s\d)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=AEG\s)(.*?)(?=\sIntegrated\s\d\d)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=AEG\s)(.*?)(?=\sIntegrated\sFrost)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Competence\s)(.*?)(?=\s\d\dcm\sCeramic)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Competence\s)(.*?)(?=\s\dcm\sCeramic)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=AEG\s)(.*?)(?=\sFully\sIntegrated)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=AEG\s)(.*?)(?=\s\d\dcm\sInduction)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=AEG\s)(.*?)(?=\s\dcm\sInduction)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=AEG\s)(.*?)(?=\s\d\dcm\sGas)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=AEG\s)(.*?)(?=\s\dcm\sGas)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=AEG\s)(.*?)(?=\sIntegrated\sUpright)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=AEG\s)(.*?)(?=\s\d\d\scm\sChimney)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=AEG\s)(.*?)(?=\sBuilt\sIn)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=AEG\s)(.*?)(?=\sBuilt\sUnder)")

        #Baumatic
        if response.xpath ('//h1[@class="productName_title"]/text()[starts-with(.,"Baumatic")]'):
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Baumatic\s)(.*?)(?=\s{1,2}[0-9])")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Baumatic\s)(.*?)(?=\sBuilt)")
        
        #beko
        if response.xpath ('//h1[@class="productName_title"]/text()[starts-with(.,"Beko")]'):
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=RecycledNet.\s)(.*?)(?=\sBuilt)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=HarvestFresh\s)(.*?)(?=\sIntegrated)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Beko\s)(.*?)(?=\Telescopic)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Beko\s)(.*?)(?=\sIntegrated)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Beko\s)(.*?)(?=\sFully)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Beko\s)(.*?)(?=\sBuilt)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Beko\s)(.*?)(?=\s{1,2}[0-9])")
        
        #Bosch
        if response.xpath ('//h1[@class="productName_title"]/text()[starts-with(.,"Bosch")]'):
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Serie\s[0-9]\s)(.*?)(?=\sIntegrated)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Serie\s[0-9]\s)(.*?)(?=\sFully)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Serie\s[0-9]\s)(.*?)(?=\sBuilt)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Serie\s[0-9]\s)(.*?)(?=\sAngled)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Serie\s[0-9]\s)(.*?)(?=\s{1,2}[0-9])")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Sander\s)(.*?)(?=\s)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Rotak\s)(.*?)(?=\sRotary)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Rotak\s)(.*?)(?=\sLawnmower)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Plate\s)(.*?)(?=\s)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Hedgecutter\s)(.*?)(?=\s)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Bosch\s)(.*?)(?=\sWifi)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Bosch\s)(.*?)(?=\sShears)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Bosch\s)(.*?)(?=\sset)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Bosch\s)(.*?)(?=\sRandom)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Bosch\s)(.*?)(?=\sQuite)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Bosch\s)(.*?)(?=\sMulti)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Bosch\s)(.*?)(?=\sLi-ion)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Bosch\s)(.*?)(?=\sHeavy)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Bosch\s)(.*?)(?=\sGlue)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Bosch\s)(.*?)(?=\sElectric)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Bosch\s)(.*?)(?=\sCordless)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Bosch\s)(.*?)(?=\sCorded)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Bosch\s)(.*?)(?=\sBuilt)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Bosch\s)(.*?)(?=\sBenchdrill)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Bosch\s)(.*?)(?=\sBelt)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Bosch\s)(.*?)(?=\sBattery)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Bosch\s)(.*?)(?=\sBaretool)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Bosch\s)(.*?)(?=\s{1,2}[0-9])")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Bosch\s)(.*?)(?=\s)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Knife\s\-\s)(.*?)(?=\s)")
        
        #Candy
        if response.xpath ('//h1[@class="productName_title"]/text()[starts-with(.,"Candy")]'):
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Rapido\s)(.*?)(?=\sWifi)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Pro\s)(.*?)(?=\sWifi)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Candy\s)(.*?)(?=\sWifi)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Candy\s)(.*?)(?=\sSlimline)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Candy\s)(.*?)(?=\sIntegrated)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Candy\s)(.*?)(?=\sBuilt)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Candy\s)(.*?)(?=\s{1,2}[0-9])")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Candy\s)(.*?)(?=\s[0-9]Kg)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Ultra\s)(.*?)(?=\s[0-9]Kg)")
        
        #Elica
        if response.xpath ('//h1[@class="productName_title"]/text()[starts-with(.,"Elica")]'):
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Elica\s)(.*?)(?=\s{1,2}[0-9])")
        
        #Hisense
        if response.xpath ('//h1[@class="productName_title"]/text()[starts-with(.,"Hisense")]'):
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Hisense\s)(.*?)(?=\sIntegrated)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Hisense\s)(.*?)(?=\sFully)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Hisense\s)(.*?)(?=\sBuilt)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Hisense\s)(.*?)(?=\sAmerican)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Hisense\s)(.*?)(?=\s{1,2}[0-9])")
        
        #Hoover
        if response.xpath ('//h1[@class="productName_title"]/text()[starts-with(.,"Hoover")]'):
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Hoover\s)(.*?)(?=\sBuilt)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=LITE\s)(.*?)(?=\sIntegrated)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=[0-9]\s)(.*?)(?=\sBuilt)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=[0-9]\s)(.*?)(?=\s{1,2}[0-9])")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=CERAMIC\s)(.*?)(?=\s{1,2}[0-9])")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=INDUCTION\s)(.*?)(?=\s{1,2}[0-9])")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=GAS\s)(.*?)(?=\s{1,2}[0-9])")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Hoover\s)(.*?)(?=\s{1,2}[0-9])")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=[0-9]\s)(.*?)(?=\sIntegrated)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=[0-9]\s)(.*?)(?=\sWifi)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Hoover\s)(.*?)(?=\sFully)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Hoover\s)(.*?)(?=\sIntegrated)")
        
        #Hotpoint
        if response.xpath ('//h1[@class="productName_title"]/text()[starts-with(.,"Hotpoint")]'):
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Hotpoint\s)(.*?)(?=\sMicrowave)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Hotpoint\s)(.*?)(?=\sIntegrated)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Hotpoint\s)(.*?)(?=\sFully)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Hotpoint\s)(.*?)(?=\sBuilt)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Hotpoint\s)(.*?)(?=\s{1,2}[0-9])")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Class\s[0-9]\s)(.*?)(?=\sBuilt)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=ActiveCook\s)(.*?)(?=\s{1,2}[0-9])")
        
        #Indesit
        if response.xpath ('//h1[@class="productName_title"]/text()[starts-with(.,"Indesit")]'):
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Indesit\s)(.*?)(?=\sIntegrated)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Indesit\s)(.*?)(?=\sFully)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Indesit\s)(.*?)(?=\sCooker)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Indesit\s)(.*?)(?=\sBuilt)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Indesit\s)(.*?)(?=\s{1,2}[0-9])")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Aria\s)(.*?)(?=\sBuilt)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Aria\s)(.*?)(?=\s{1,2}[0-9])")

        #Leisure
        if response.xpath ('//h1[@class="productName_title"]/text()[starts-with(.,"Leisure")]'):
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Leisure\s)(.*?)(?=\s{1,2}[0-9])")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Cookmaster\s)(.*?)(?=\s{1,2}[0-9])")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=[0-9]\s)(.*?)(?=\s{1,2}[0-9])")

        #NEFF
        if response.xpath ('//h1[@class="productName_title"]/text()[starts-with(.,"NEFF")]'):
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=NEFF\s)(.*?)(?=\sIntegrated)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=\sN\d\d\s)(.*?)(?=\sWifi)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=\sN\d\d\s)(.*?)(?=\sE)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Slide&Hide..\s)(.*?)(?=\sBuilt)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=\sN\d\d\s)(.*?)(?=\sBuilt)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=\sN\d\d\s)(.*?)(?=\sFully)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=\sN\d\d\s)(.*?)(?=\sIntegrated)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=\sN\d\d\s)(.*?)(?=\s{1,2}[0-9])")

        #Rangemaster
        if response.xpath ('//h1[@class="productName_title"]/text()[starts-with(.,"Rangemaster")]'):
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Toledo\+\s)(.*?)(?=\s{1,2}[0-9])")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Rangemaster\s)(.*?)(?=\sRangecooker)")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Rangemaster\s)(.*?)(?=\s{1,2}[0-9])")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Plus\s)(.*?)(?=\s{1,2}[0-9])")
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Esprit\s)(.*?)(?=\s{1,2}[0-9])")

        #Samsung
        if response.xpath ('//h1[@class="productName_title"]/text()[starts-with(.,"Samsung")]'):
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=[0-9]\s)(.*?)(?=\sAmerican)")

        #Zanussi
        if response.xpath ('//h1[@class="productName_title"]/text()[starts-with(.,"Zanussi")]'):
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Zanussi\s)(.*?)(?=\sBuilt)")

        #Smeg
        if response.xpath ('//h1[@class="productName_title"]/text()[starts-with(.,"Smeg")]'): 
            BB.add_xpath ('sku','//h1[@class="productName_title"]/text()', re=r"(?<=Smeg\s)(.*?)(?=\s{1,2}[0-9])")

        else: 
            BB.add_xpath ('sku','//div[@class="externalSku"]/text()', re=r"(.+)")
         # Administration Fiels
        BB.add_value('url', response.url)
        BB.add_value('project', self.settings.get('BOT_NAME'))
        BB.add_value('useragent', self.settings.get('USER_AGENT'))
        BB.add_value('spider', self.name)
        BB.add_value('server', socket.gethostname())
        BB.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return BB.load_item()

        