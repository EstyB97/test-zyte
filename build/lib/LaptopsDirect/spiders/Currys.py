# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
import socket
import scrapy
import re
from scrapy import selector
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from LaptopsDirect.items import LaptopsdirectItem
import logging
from scrapy.loader.processors import TakeFirst
from requests import get

ip = get('https://api.ipify.org').text
get('https://www.duckdns.org/update?domains=cabbage51&token=96e0eeee-e2f3-4788-a861-dfeac8b55126&ip='.format(ip))

#Custom downloader middleware uses a proxy to disguise where the request is coming from. Proxy has to be UK based or will only work for a couple of runs. Limited number of runs per proxy per day as there is some sort of
#counting in place on the number of page requests per IP. If a custom user agent is used they will block it automatically. Conditional based fields are listed below and Regex on the import into our data
#extracts out the first found node. Nodes in this spider return blank ([]) rather than NULL through the API due to the use of the re library for regex processing.

class CurrysSpider(SitemapSpider):
    name = 'Currys'
    custom_settings = { 
        'DOWNLOADER_MIDDLEWARES' : {
            'LaptopsDirect.middlewares.CustomProxyMiddleware': 350,
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 400,
        },
        'CLOSESPIDER_TIMEOUT' : '864000'
   }
    allowed_domains = ['currys.co.uk']
    sitemap_urls = ['https://www.currys.co.uk/robots.txt']
    #handle_httpstatus_list = [301, 302, 200]
    
    def parse(self, response):

        l = ItemLoader(item=LaptopsdirectItem(), response=response)
        #l.default_output_processor = TakeFirst()   -- Breaks the JSON on integration

        #Scrape Fields
        l.add_xpath('title', '/html/head/title/text()')

            #Look for BELLING in product title, Extract everything between INDESIT and Chest Freezer - White
        l.add_xpath('sku', '//span[starts-with(.,"BELLING")]/following::p[@class="prd-code"]/text()', re=r"[0-9]*$")
            #Look for STOVES in product title, Extract everything between INDESIT and Chest Freezer - White
        l.add_xpath('sku', '//span[starts-with(.,"STOVES")]/following::p[@class="prd-code"]/text()', re=r"[0-9]*$")

            #Look for NEFF in product title, check if the title contains N30. If it does extract the full title but then only take the 2nd word (Part Code) using Regex in Python
        l.add_xpath('sku', '//span[starts-with(.,"NEFF")]/following::span[contains(.,"N30")]', re=r"^(?:[^\s]*\s){1}([^\s]*)") 
            #Look for NEFF in product title, check if the title contains N70. If it does extract the full title but then only take the 2nd word (Part Code) using Regex in Python
        l.add_xpath('sku', '//span[starts-with(.,"NEFF")]/following::span[contains(.,"N70")]', re=r"^(?:[^\s]*\s){1}([^\s]*)") 
            
            #SKU Specific INDESIT
        l.add_xpath('sku', '//span[starts-with(.,"INDESIT")]/following::span[contains(.,"I55TM 4110 X")]', re=r"(.*)(?=70/30 Fridge Freezer - Silver)")
        l.add_xpath('sku', '//span[starts-with(.,"INDESIT")]/following::span[contains(.,"BWC 61452 W")]', re=r"(.*)(?=6 kg 1400 Spin Washing Machine - White)")
        l.add_xpath('sku', '//span[starts-with(.,"INDESIT")]/following::span[contains(.,"IZ A1.UK")]', re=r"(.*)(?=.UK.1 Integrated Undercounter Freezer)")
            
            #Look for INDESIT in product title, Extract everything between INDESIT and Chest Freezer - White
        l.add_xpath('sku', '//span[starts-with(.,"INDESIT")]/following::span[contains(.,"DCF 1A 250.1")]', re=r"(.*)(?=Chest Freezer - White)")
            #Look for INDESIT in product title, Extract everything between INDESIT and Integrated 8 kg 1200 Spin Washing Machine
        l.add_xpath('sku', '//span[starts-with(.,"INDESIT")]/following::span[contains(.,"BIWMIL81284")]', re=r"(.*)(?=Integrated 8 kg 1200)")
            #Look for INDESIT in product title, Extract everything between INDESIT and 6 KG 1400 Spin Washing Machine
        l.add_xpath('sku', '//span[starts-with(.,"INDESIT")]/following::span[contains(.,"BWC 61452 S 6 kg 1400 Spin Washing Machine")]', re=r"(.*)(?=6 kg 1400 Spin Washing Machine)")
            #Look for INDESIT in product title, Extract everything between INDESIT and .1 70/30 Fridge Freezer
        l.add_xpath('sku', '//span[starts-with(.,"INDESIT")]/following::span[contains(.,"LD70 S1 W.1 70/30 Fridge Freezer")]', re=r"(.*)(?=.1 70/30 Fridge Freezer)")
            #Look for INDESIT in product title, Extract everything between INDESIT THP and Gas Hob
        l.add_xpath('sku', '//span[starts-with(.,"INDESIT")]/following::span[contains(.,"Aria")]', re=r"(.*)(?=Gas Hob)")
            #Look for INDESIT in product title, Extract everything between INDESIT VID   and Washing Machine
        l.add_xpath('sku', '//span[starts-with(.,"INDESIT")]/following::span[contains(.,"VID  ")]', re=r"(.*)(?=Electric Induction Hob)")
            #Look for INDESIT in product title, Extract everything between INDESIT Innex  and Washing Machine
        l.add_xpath('sku', '//span[starts-with(.,"INDESIT")]/following::span[contains(.,"Innex ")]', re=r"(?<=Innex )(.*)(?=Washing Machine)")
            #Look for INDESIT in product title, Extract everything between INDESIT eXtra Baby Care and UK Slimline
        l.add_xpath('sku', '//span[starts-with(.,"INDESIT")]/following::span[contains(.,"eXtra Baby Care")]', re=r"(?<=eXtra Baby Care)(.*)(?=UK)")
            #Look for INDESIT in product title, Extract everything between INDESIT Aria and Electric Oven
        l.add_xpath('sku', '//span[starts-with(.,"INDESIT")]/following::span[contains(.,"Aria")]', re=r"(?<=Aria)(.*)(?=Electric Oven)")
            #Look for INDESIT in product title, Extract everything between Indesit and Undercounter for K Undercounter Freezer
        l.add_xpath('sku', '//span[starts-with(.,"INDESIT")]/following::span[contains(.,"Undercounter Freezer")]', re=r"(.*)(?=Undercounter Freezer)")
            #Look for INDESIT in product title, with Evo appending the part code and extract the first two words (Part Code) from the span node
        l.add_xpath('sku', 'substring(//span[starts-with(.,"INDESIT")]/following::span[contains(.,"ECO")],1,string-length(substring-before(//span[starts-with(.,"INDESIT")]/following::span[contains(.,"ECO")]," "))+string-length(substring-before(substring-after(//span[starts-with(.,"INDESIT")]/following::span[contains(.,"ECO")]," ")," "))+1)')
            #Look for INDESIT in product title, check if the title contains ecobubble. If it does extract the full title but then only take the 2nd word (Part Code) using Regex in Python
        l.add_xpath('sku', '//span[starts-with(.,"INDESIT")]/following::span[contains(.,"Ecotime")]', re=r"^(?:[^\s]*\s){1}([^\s]*)")             
            #Look for INDESIT in product title, with INF prefixing the part code and extract the (Part Code) from the span node
        l.add_xpath('sku', 'substring(//span[starts-with(.,"INDESIT")]/following::span[contains(.,"INF")],1,string-length(substring-before(//span[starts-with(.,"INDESIT")]/following::span[contains(.,"INF")]," "))+string-length(substring-before(substring-after(//span[starts-with(.,"INDESIT")]/following::span[contains(.,"INF")]," ")," "))+5)')
            #Look for INDESIT in product title, take first word (Part Code) from next span node
        l.add_xpath('sku', 'substring(//span[starts-with(.,"INDESIT")]/following::span[1],1,string-length(substring-before(//span[starts-with(.,"INDESIT")]/following::span[1]," ")))')
            #Look for Beko in product title, check if the title contains Pro Aquatech. If it does extract the full title but then only take the 3rd word (Part Code) using Regex in Python
        l.add_xpath('sku', '//span[starts-with(.,"Beko")]/following::span[contains(.,"Pro AquaTech")]', re=r"^(?:[^\s]*\s){2}([^\s]*)")
            #Look for Beko in product title, check if the title contains Pro. If it does extract the full title but then only take the 2nd word (Part Code) using Regex in Python
        l.add_xpath('sku', '//span[starts-with(.,"Beko")]/following::span[contains(.,"Pro")]', re=r"^(?:[^\s]*\s){1}([^\s]*)")    
            #Look for Beko in product title, take first word (Part Code) from next span node
        l.add_xpath('sku', 'substring(//span[starts-with(.,"BEKO")]/following::span[1],1,string-length(substring-before(//span[starts-with(.,"BEKO")]/following::span[1]," ")))')
            #Look for LG in product title, take first word (Part Code) from next span node
        l.add_xpath('sku', 'substring(//span[starts-with(.,"LG")]/following::span[1],1,string-length(substring-before(//span[starts-with(.,"LG")]/following::span[1]," ")))')
            #Look for LOGIK in product title, take first word (Part Code) from next span node
        l.add_xpath('sku', 'substring(//span[starts-with(.,"LOGIK")]/following::span[1],1,string-length(substring-before(//span[starts-with(.,"LOGIK")]/following::span[1]," ")))')
            #Look for SMEG Concert SUK91MFX9 in product title, Extract everything between SMEG Concert and 90 cm Dual Fuel Range Cooker
        l.add_xpath('sku', '//span[starts-with(.,"SMEG")]/following::span[contains(.,"Concert SUK91MFX9")]', re=r"(?<=Concert)(.*)(?=90 cm Dual Fuel Range Cooker)")
            #Look for SMEG in product title, take first word (Part Code) from next span node
        l.add_xpath('sku', 'substring(//span[starts-with(.,"SMEG")]/following::span[1],1,string-length(substring-before(//span[starts-with(.,"SMEG")]/following::span[1]," ")))')
            #Look for HAIER in product title, take first word (Part Code) from next span node
        l.add_xpath('sku', 'substring(//span[starts-with(.,"HAIER")]/following::span[1],1,string-length(substring-before(//span[starts-with(.,"HAIER")]/following::span[1]," ")))')
            #Look for KENWOOD in product title, take first word (Part Code) from next span node
        l.add_xpath('sku', 'substring(//span[starts-with(.,"KENWOOD")]/following::span[1],1,string-length(substring-before(//span[starts-with(.,"KENWOOD")]/following::span[1]," ")))')
            #Look for GRUNDIG in product title, take first word (Part Code) from next span node
        l.add_xpath('sku', 'substring(//span[starts-with(.,"GRUNDIG")]/following::span[1],1,string-length(substring-before(//span[starts-with(.,"GRUNDIG")]/following::span[1]," ")))')
            #Look for HISENSE in product title, take first word (Part Code) from next span node
        l.add_xpath('sku', 'substring(//span[starts-with(.,"HISENSE")]/following::span[1],1,string-length(substring-before(//span[starts-with(.,"HISENSE")]/following::span[1]," ")))')
            
            #Samsung SKU Specific Mapping
        l.add_xpath('sku', '//span[starts-with(.,"SAMSUNG")]/following::span[contains(.,"Series 5 DV90TA040AX/EU")]', re=r"^(?:[^\s]*\s){2}([^\s]*)")
        l.add_xpath('sku', '//span[starts-with(.,"SAMSUNG")]/following::span[contains(.,"Series 5 ecobubble WW80TA046TH/EU")]', re=r"^(?:[^\s]*\s){3}([^\s]*)")
        l.add_xpath('sku', '//span[starts-with(.,"SAMSUNG")]/following::span[contains(.,"RS3000 RS50N3513BC/EU")]', re=r"^(?:[^\s]*\s){2}([^\s]*)")
        l.add_xpath('sku', '//span[starts-with(.,"SAMSUNG")]/following::span[contains(.,"Dual Cook Flex NV75N5671RS")]', re=r"^(?:[^\s]*\s){4}([^\s]*)")
        l.add_xpath('sku', '//span[starts-with(.,"SAMSUNG")]/following::span[contains(.,"Series 9 DV90T8240SX/S1")]', re=r"^(?:[^\s]*\s){2}([^\s]*)")
        l.add_xpath('sku', '//span[starts-with(.,"SAMSUNG")]/following::span[contains(.,"Series 5+ Auto Dose WW10T534DAN/S1")]', re=r"^(?:[^\s]*\s){5}([^\s]*)")
        l.add_xpath('sku', '//span[starts-with(.,"SAMSUNG")]/following::span[contains(.,"Series 6 AddWash + Auto Dose WW10T684DLH/S1")]', re=r"^(?:[^\s]*\s){7}([^\s]*)")
        l.add_xpath('sku', '//span[starts-with(.,"SAMSUNG")]/following::span[contains(.,"Series 5+ AddWash WW90T554DAN/S1")]', re=r"^(?:[^\s]*\s){4}([^\s]*)")
        l.add_xpath('sku', '//span[starts-with(.,"SAMSUNG")]/following::span[contains(.,"Series 6 AddWash + Auto Dose WW80T684DLH/S1")]', re=r"^(?:[^\s]*\s){7}([^\s]*)")
        l.add_xpath('sku', '//span[starts-with(.,"SAMSUNG")]/following::span[contains(.,"Series 5 ecobubble WW80TA046AX/EU")]', re=r"^(?:[^\s]*\s){4}([^\s]*)")
        l.add_xpath('sku', '//span[starts-with(.,"SAMSUNG")]/following::span[contains(.,"Series 5 ecobubble WW70TA046TE/EU")]', re=r"^(?:[^\s]*\s){4}([^\s]*)")
        l.add_xpath('sku', '//span[starts-with(.,"SAMSUNG")]/following::span[contains(.,"Series 6 AddWash + Auto Dose WW10T684DLN/S1")]', re=r"^(?:[^\s]*\s){7}([^\s]*)")

            #Look for Samsung in product title, check if the title contains Series 5 ecobubble then take the 4th word
        l.add_xpath('sku', '//span[starts-with(.,"SAMSUNG")]/following::span[contains(.,"Series 5 ecobubble")]', re=r"^(?:[^\s]*\s){4}([^\s]*)")
            #Look for Samsung in product title, check if the title contains series 6 addwash then take the 4th word
        l.add_xpath('sku', '//span[starts-with(.,"SAMSUNG")]/following::span[contains(.,"Series 6 AddWash")]', re=r"^(?:[^\s]*\s){4}([^\s]*)")
            #Look for SAMSUNG in product title, check if the title contains Dual Cook. If it does extract the full title but then only take the 3rd word (Part Code) using Regex in Python
        l.add_xpath('sku', '//span[starts-with(.,"SAMSUNG")]/following::span[contains(.,"Dual Cook")]', re=r"^(?:[^\s]*\s){2}([^\s]*)")
            #Look for SAMSUNG in product title, check if the title contains AddWash. If it does extract the full title but then only take the 2nd word (Part Code) using Regex in Python
        l.add_xpath('sku', '//span[starts-with(.,"SAMSUNG")]/following::span[contains(.,"AddWash")]', re=r"^(?:[^\s]*\s){1}([^\s]*)")            
            #Look for SAMSUNG in product title, check if the title contains ecobubble. If it does extract the full title but then only take the 2nd word (Part Code) using Regex in Python
        l.add_xpath('sku', '//span[starts-with(.,"SAMSUNG")]/following::span[contains(.,"ecobubble")]', re=r"^(?:[^\s]*\s){1}([^\s]*)")  
            #Look for SAMSUNG in product title, check if the title contains QuickDrive. If it does extract the full title but then only take the 4th word (Part Code) using Regex in Python
        l.add_xpath('sku', '//span[starts-with(.,"SAMSUNG")]/following::span[contains(.,"QuickDrive")]', re=r"^(?:[^\s]*\s){3}([^\s]*)")
            #Look for SAMSUNG in product title, check if the title contains Dual Cook Flex. If it does extract the full title but then only take the 4th word (Part Code) using Regex in Python
        l.add_xpath('sku', '//span[starts-with(.,"SAMSUNG")]/following::span[contains(.,"Dual Cook Flex")]', re=r"^(?:[^\s]*\s){4}([^\s]*)")    
            #Look for SAMSUNG in product title, check if the title contains RS8000. If it does extract the full title but then only take the 2nd word (Part Code) using Regex in Python
        l.add_xpath('sku', '//span[starts-with(.,"SAMSUNG")]/following::span[contains(.,"RS8000")]', re=r"^(?:[^\s]*\s){1}([^\s]*)")
           #Look for SAMSUNG in product title, check if the title contains Series. If it does extract the full title but then only take the 3rd word (Part Code) using Regex in Python
        l.add_xpath('sku', '//span[starts-with(.,"SAMSUNG")]/following::span[contains(.,"Series")]', re=r"^(?:[^\s]*\s){2}([^\s]*)") 
            #Look for SAMSUNG in product title, take first word (Part Code) from next span node
        l.add_xpath('sku', 'substring(//span[starts-with(.,"SAMSUNG")]/following::span[1],1,string-length(substring-before(//span[starts-with(.,"SAMSUNG")]/following::span[1]," ")))')
            
            #Look for AEG in product title, check if the title contains SenseCook. If it does extract the full title but then only take the 2nd word (Part Code) using Regex in Python
        l.add_xpath('sku', '//span[starts-with(.,"AEG")]/following::span[contains(.,"SenseCook")]', re=r"^(?:[^\s]*\s){1}([^\s]*)") 
            #Look for AEG in product title, check if the title contains ProSense. If it does extract the full title but then only take the 2nd word (Part Code) using Regex in Python
        l.add_xpath('sku', '//span[starts-with(.,"AEG")]/following::span[contains(.,"ProSense")]', re=r"^(?:[^\s]*\s){1}([^\s]*)")               
            #Look for AEG in product title, check if the title contains AirDry. If it does extract the full title but then only take the 3rd word (Part Code) using Regex in Python
        l.add_xpath('sku', '//span[starts-with(.,"AEG")]/following::span[contains(.,"AirDry")]', re=r"^(?:[^\s]*\s){2}([^\s]*)")    
            #Look for AEG in product title, take first word (Part Code) from next span node
        l.add_xpath('sku', 'substring(//span[starts-with(.,"AEG")]/following::span[1],1,string-length(substring-before(//span[starts-with(.,"AEG")]/following::span[1]," ")))')
            #Look for BOSCH in product title, check if the title contains Serie 4 Flexxo. If it does extract the full title but then only take the 4th word (Part Code) using Regex in Python
        l.add_xpath('sku', '//span[starts-with(.,"BOSCH")]/following::span[contains(.,"Serie 4 Flexxo")]', re=r"^(?:[^\s]*\s){3}([^\s]*)")
            #Look for BOSCH in product title, check if the title contains Serie. If it does extract the full title but then only take the 3rd word (Part Code) using Regex in Python
        l.add_xpath('sku', '//span[starts-with(.,"BOSCH")]/following::span[contains(.,"Serie")]', re=r"^(?:[^\s]*\s){2}([^\s]*)")
            #Look for BOSCH in product title, take first word (Part Code) from next span node
        l.add_xpath('sku', 'substring(//span[starts-with(.,"BOSCH")]/following::span[1],1,string-length(substring-before(//span[starts-with(.,"BOSCH")]/following::span[1]," ")))')
            
                #SKU SPECIFIC HOTPOINT 

        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"H55RM 1110 W UK")]', re=r"(.*)(?=UK Undercounter Fridge - White)")
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"MWH 1331 B")]', re=r"(.*)(?=Solo Microwave - Black)")
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"CIS 640 B")]', re=r"(.*)(?=Electric Induction Hob - Black)")
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"HBC 2B19 X")]', re=r"(.*)(?=Full-size Semi-Integrated Dishwasher - Inox)")
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"Class 3 MD 344 IX H")]', re=r"(?<=Class 3)(.*)(?=Built-in Microwave with Grill - Stainless Steel)")
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"UH8 F1C W UK.1")]', re=r"(.*)(?=.1 Tall Freezer - White)")
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"UH8 F1C W UK.1")]', re=r"(.*)(?=.1 Tall Freezer - White)")
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"MWH 301 B")]', re=r"(.*)(?=Solo Microwave - Black)")
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"HR 612 C H")]', re=r"(.*)(?=Electric Ceramic Hob - Black)")
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"MWH 2621 MB Solo Microwave - Black")]', re=r"(.*)(?=Solo Microwave - Black)")
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"HQ9 U1BL UK")]', re=r"(.*)(?=UK Fridge Freezer - Black & Inox)")
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"BIWMIL81284")]', re=r"(.*)(?=Integrated 8 kg 1200 Spin Washing Machine)")
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"HZ A1.UK.1")]', re=r"(.*)(?=.1 Integrated Undercounter Freezer)")
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"PHVP 8.7F LT K")]', re=r"(.*)(?=Canopy Cooker Hood - Black)")
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"FFU4D.1 X")]', re=r"(.*)(?=Fridge Freezer)")
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"HM 7030 E C AA O3")]', re=r"(.*)(?=.1 Integrated 70/30)")
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"UD 514 IX")]', re=r"(.*)(?=Accessory Drawer)")
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"LAL85 FF1I W WTD")]', re=r"(.*)(?=.1 50/50 Fridge Freezer)")
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"SXBHE 924 WD")]', re=r"(.*)(?=American-Style Fridge Freezer)")
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"HR 7011 B H")]', re=r"(.*)(?=Electric Ceramic Hob)")
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"CM 5038 IX H")]', re=r"(.*)(?=Built-in Filter Coffee Machine)") 
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"FFU4D.1 K")]', re=r"(.*)(?=Fridge Freezer)")   
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"PCN 642 /H(BK)")]', re=r"(.*)(?=Gas Hob)")   
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"PAS 642/H")]', re=r"(.*)(?=Gas Hob)")    
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"PCN 752 U/IX/H")]', re=r"(.*)(?=Gas Hob)")            
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"HSFE 1B19 UK")]', re=r"(.*)(?=Slimline Dishwasher)")
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"HIC 3C26 W F")]', re=r"(.*)(?=Integrated)")
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"RD 966 JKD UK")]', re=r"(.*)(?=UK Washer Dryer)")
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"RD 1076 JD UK")]', re=r"(.*)(?=UK Washer Dryer)")
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"Aquarius HBNF 55181 S UK")]', re=r"(?<=Aquarius)(.*)(?=UK 50/50 Fridge Freezer)")
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"Ultima HUG61X 60")]', re=r"(?<=Ultima )(.*)(?=60 cm Gas Cooker)")
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"NT M10 81WK UK")]', re=r"(.*)(?=UK 8 kg Heat Pump)")
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"MWH 2734 B")]', re=r"(.*)(?=Combination Microwave)")
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"HBC 2B19 Full-size")]', re=r"(.*)(?=Full-size Semi-Integrated)")
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"MP 676 IX H Built-in")]', re=r"(.*)(?=Built-in Combination)")
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"Ultima S-Line BI WDHL 7128 UK")]', re=r"(?<=Ultima S-Line)(.*)(?=UK)")
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"MP 676 IX H Built-in")]', re=r"(.*)(?=UK Full-size Dishwasher)")
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"PHGC7.4 FLMX Chimney")]', re=r"(.*)(?=Chimney Cooker Hood)")
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"MN 314 IX H Built-in Microwave")]', re=r"(.*)(?=Built-in Microwave with Grill)")
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"Futura FDL 9640 K")]', re=r"(?<=Futura)(.*)(?=9 kg Washer Dryer)")
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"FDL 8640P")]', re=r"(?<=FDL)(.*)(?=9 kg Washer Dryer)")
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"SH6 1Q W UK.1")]', re=r"(.*)(?=UK.1 Tall Fridge)")
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"BCB 8020 AA F C.1 Integrated")]', re=r"(.*)(?=.1 Integrated 70/30)")
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"HFC 3C26 W UK Full-size Dishwasher")]', re=r"(.*)(?=UK Full-size Dishwasher)")
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"Futura FDL 9640 G")]', re=r"(?<=Futura)(.*)(?=9 kg Washer Dryer)")
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"NM10 944 GS UK 9 kg")]', re=r"(.*)(?=UK 9 kg 1400 Spin)")
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"ActiveCare NM11 946 WC A 9")]', re=r"(?<=ActiveCare)(.*)(?=9 kg 1400 Spin Washing Machine)")
        
        #trial HOTPOINT
        l.add_xpath('sku', '//h1[@class="product-name"][contains(.,"HOTPOINT")]/text()', re=r"(?<=HOTPOINT\s)(.*)(?=\s\d\d\skg)")
        l.add_xpath('sku', '//h1[@class="product-name"][contains(.,"HOTPOINT")]/text()', re=r"(?<=HOTPOINT\s)(.*)(?=\s\d\skg)")
        l.add_xpath('sku', '//h1[@class="product-name"][contains(.,"HOTPOINT")]/text()', re=r"(?<=HOTPOINT\s)(.*)(?=\sElectric\sCeramic)")
        l.add_xpath('sku', '//h1[@class="product-name"][contains(.,"HOTPOINT")]/text()', re=r"(?<=HOTPOINT\s)(.*)(?=\sGas)")
        l.add_xpath('sku', '//h1[@class="product-name"][contains(.,"HOTPOINT")]/text()', re=r"(?<=HOTPOINT\s)(.*)(?=\s\d\d\scm)")
        l.add_xpath('sku', '//h1[@class="product-name"][contains(.,"HOTPOINT")]/text()', re=r"(?<=HOTPOINT\s)(.*)(?=\s\d\sTall)")
        l.add_xpath('sku', '//h1[@class="product-name"][contains(.,"HOTPOINT")]/text()', re=r"(?<=Class\s\d\s)(.*)(?=\sElectric\sOven)")
        l.add_xpath('sku', '//h1[@class="product-name"][contains(.,"HOTPOINT")]/text()', re=r"(?<=HOTPOINT\s)(.*)(?=\sChimney)")
        l.add_xpath('sku', '//h1[@class="product-name"][contains(.,"HOTPOINT")]/text()', re=r"(?<=HOTPOINT\s)(.*)(?=\sFull\-size)")
        l.add_xpath('sku', '//h1[@class="product-name"][contains(.,"HOTPOINT")]/text()', re=r"(?<=HOTPOINT\s)(.*)(?=\sMicrowave\swith)")
        l.add_xpath('sku', '//h1[@class="product-name"][contains(.,"HOTPOINT")]/text()', re=r"(?<=HOTPOINT\s)(.*)(?=\sIntegrated)")
        l.add_xpath('sku', '//h1[@class="product-name"][contains(.,"HOTPOINT")]/text()', re=r"(?<=HOTPOINT\s)(.*)(?=\sSolo\sMicrowave)")
        l.add_xpath('sku', '//h1[@class="product-name"][contains(.,"HOTPOINT")]/text()', re=r"(?<=HOTPOINT\s)(.*)(?=\s\d\d\/\d\d)")
        l.add_xpath('sku', '//h1[@class="product-name"][contains(.,"HOTPOINT")]/text()', re=r"(?<=HOTPOINT\s)(.*)(?=\sUndercounter)")
        l.add_xpath('sku', '//h1[@class="product-name"][contains(.,"HOTPOINT")]/text()', re=r"(?<=HOTPOINT\s)(.*)(?=\sBuilt-in)")
        l.add_xpath('sku', '//h1[@class="product-name"][contains(.,"HOTPOINT")]/text()', re=r"(?<=Built-In\s)(.*)(?=\sWarming\sDrawer)")
        l.add_xpath('sku', '//h1[@class="product-name"][contains(.,"HOTPOINT")]/text()', re=r"(?<=HOTPOINT\s)(.*)(?=\sFridge)")
        l.add_xpath('sku', '//h1[@class="product-name"][contains(.,"HOTPOINT")]/text()', re=r"(?<=Class\s\d\s)(.*)(?=\sElectric)")
        l.add_xpath('sku', '//h1[@class="product-name"][contains(.,"HOTPOINT")]/text()', re=r"(?<=HOTPOINT\s)(.*)(?=\sCombination)")
        l.add_xpath('sku', '//h1[@class="product-name"][contains(.,"HOTPOINT")]/text()', re=r"(?<=Class\s\d\s)(.*)(?=\sBuilt-in)")
        l.add_xpath('sku', '//h1[@class="product-name"][contains(.,"HOTPOINT")]/text()', re=r"(?<=HOTPOINT\s)(.*)(?=\sChest)")
        l.add_xpath('sku', '//h1[@class="product-name"][contains(.,"HOTPOINT")]/text()', re=r"(?<=Extraspace\s)(.*)(?=\sMicrowave)")
        l.add_xpath('sku', '//h1[@class="product-name"][contains(.,"HOTPOINT")]/text()', re=r"(?<=S\-Line\s)(.*)(?=\s\d\d\skg)")
        l.add_xpath('sku', '//h1[@class="product-name"][contains(.,"HOTPOINT")]/text()', re=r"(?<=S\-Line\s)(.*)(?=\s\d\skg)")
        l.add_xpath('sku', '//h1[@class="product-name"][contains(.,"HOTPOINT")]/text()', re=r"(?<=HOTPOINT\s)(.*)(?=\sSlimline)")
        l.add_xpath('sku', '//h1[@class="product-name"][contains(.,"HOTPOINT")]/text()', re=r"(?<=Amelia\s)(.*)(?=\s\d\d\scm)")
        l.add_xpath('sku', '//h1[@class="product-name"][contains(.,"HOTPOINT")]/text()', re=r"(?<=Cannon\s)(.*)(?=\s\d\d\scm)")
        l.add_xpath('sku', '//h1[@class="product-name"][contains(.,"HOTPOINT")]/text()', re=r"(?<=Aquarius\s)(.*)(?=\sIntegrated\sUndercounter)")
        l.add_xpath('sku', '//h1[@class="product-name"][contains(.,"HOTPOINT")]/text()', re=r"(?<=Core\s)(.*)(?=\s\d\skg)")
        l.add_xpath('sku', '//h1[@class="product-name"][contains(.,"HOTPOINT")]/text()', re=r"(?<=Core\s)(.*)(?=\s\d\d\skg)")
        l.add_xpath('sku', '//h1[@class="product-name"][contains(.,"HOTPOINT")]/text()', re=r"(?<=HOTPOINT\s)(.*)(?=\sCanopy)")
        l.add_xpath('sku', '//h1[@class="product-name"][contains(.,"HOTPOINT")]/text()', re=r"(?<=HOTPOINT\s)(.*)(?=\sCompact)")
        l.add_xpath('sku', '//h1[@class="product-name"][contains(.,"HOTPOINT")]/text()', re=r"(?<=HOTPOINT\s)(.*)(?=\sAmerican)")
        l.add_xpath('sku', '//h1[@class="product-name"][contains(.,"HOTPOINT")]/text()', re=r"(?<=Gentlepower)(.*)(?=\s\d\skg)")
        l.add_xpath('sku', '//h1[@class="product-name"][contains(.,"HOTPOINT")]/text()', re=r"(?<=Gentlepower)(.*)(?=\s\d\d\skg)")
        l.add_xpath('sku', '//h1[@class="product-name"][contains(.,"HOTPOINT")]/text()', re=r"(?<=Day\d\s)(.*)(?=\sAqua\s)")
        l.add_xpath('sku', '//h1[@class="product-name"][contains(.,"HOTPOINT")]/text()', re=r"(?<=Active\sCare)(.*)(?=\s\d\skg)")
        l.add_xpath('sku', '//h1[@class="product-name"][contains(.,"HOTPOINT")]/text()', re=r"(?<=Active\sCare)(.*)(?=\s\d\d\skg)")
        l.add_xpath('sku', '//h1[@class="product-name"][contains(.,"HOTPOINT")]/text()', re=r"(?<=Day1\s)(.*)(?=\s\d\d\/\d\d)")
        l.add_xpath('sku', '//h1[@class="product-name"][contains(.,"HOTPOINT")]/text()', re=r"(?<=ActiveCare\s)(.*)(?=\sWifi-enabled)")
        l.add_xpath('sku', '//h1[@class="product-name"][contains(.,"HOTPOINT")]/text()', re=r"(?<=Direct\sFlame\s)(.*)(?=\sGas)")

                #END OF SKU SPECIFIC HOTPOINT

                #SKU SPECIFIC HOOVER/CANDY

        l.add_xpath('sku', '//span[starts-with(.,"HOOVER")]/following::span[contains(.,"H-HOB 300 GAS HHG7MX")]', re=r"(?<=300 GAS )(.*)(?=Gas Hob)")
        l.add_xpath('sku', '//span[starts-with(.,"HOOVER")]/following::span[contains(.,"H-OVEN 500 PLUS HOAZ8673")]', re=r"(?<=500 PLUS )(.*)(?=Electric Oven)")
        l.add_xpath('sku', '//span[starts-with(.,"HOOVER")]/following::span[contains(.,"H-HOB 500 CERAMIC ")]', re=r"(?<=H-HOB 500 CERAMIC )(.*)(?=Electric Ceramic Hob)")

                #END OF SKU SPECIFIC HOOVER/CANDY
            
            #Look for HOTPOINT in product title, Extract everything between Day1 and 70/30
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"Day1")]', re=r"(?<=Day1)(.*)(?=70/30)")
            #Look for HOTPOINT in product title, Extract everything between ActiveCare and UK
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"ActiveCare")]', re=r"(?<=ActiveCare)(.*)(?=UK)")
            #Look for HOTPOINT in product title, Extract everything between Newstyle and Electric for Ovens
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"Newstyle")]', re=r"(?<=Newstyle)(.*)(?=Electric)")
            #Look for HOTPOINT in product title, Extract everything between Direct Flame and Electric for Ovens
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"Direct Flame")]', re=r"(?<=Direct Flame)(.*)(?=Electric)")
            #Look for HOTPOINT in product title, Extract everything between Activecook and Electric for Ovens
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"Activecook")]', re=r"(?<=Activecook)(.*)(?=Electric)")
            #Look for HOTPOINT in product title, Extract everything between Class 2 and Electric for Ovens
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"Class 2")]', re=r"(?<=Class 2 )(.*)(?= Electric)")
            #Look for HOTPOINT in product title, Extract everything between Class 4 and Electric for Ovens
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"Class 4")]', re=r"(?<=Class 4 )(.*)(?= Electric)")
            #Look for HOTPOINT in product title, Extract everything between Class 6 and Electric for Ovens
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"Class 6")]', re=r"(?<=Class 6 )(.*)(?= Electric)")
            #Look for HOTPOINT in product title, check if the title contains Smart. If it does extract the full title but then only take the 2nd word (Part Code) using Regex in Python
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"Smart")]', re=r"^(?:[^\s]*\s){1}([^\s]*)")  
            #Look for HOTPOINT in product title, check if the title contains Aqualtis. If it does extract the full title but then only take the 2nd word (Part Code) using Regex in Python
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"Aqualtis")]', re=r"^(?:[^\s]*\s){1}([^\s]*)")  
            #Look for HOTPOINT in product title, check if the title contains Aquarius. If it does extract the full title but then only take the 2nd word (Part Code) using Regex in Python
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"Aquarius")]', re=r"^(?:[^\s]*\s){1}([^\s]*)")
            #Look for HOTPOINT in product title, check if the title contains Ultima. If it does extract the full title but then only take the 3rd word (Part Code) using Regex in Python
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"Ultima")]', re=r"^(?:[^\s]*\s){2}([^\s]*)")
            #Look for HOTPOINT in product title, check if the title contains First Edition. If it does extract the full title but then only take the 3rd word (Part Code) using Regex in Python
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"First Edition")]', re=r"^(?:[^\s]*\s){2}([^\s]*)")
            #Look for HOTPOINT in product title, with NSW appending the part code and extract the first three words (Part Code) from the span node
        #l.add_xpath('sku', 'substring(//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"NSW")],1,string-length(substring-before(//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"NSW")]," "))+string-length(substring-before(substring-after(//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"NSW")]," ")," "))+4)')
            #Look for HOTPOINT in product title, with PCN appending the part code and extract the first three words (Part Code) from the span node
        #l.add_xpath('sku', 'substring(//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"PCN")],1,string-length(substring-before(//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"PCN")]," "))+string-length(substring-before(substring-after(//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"PCN")]," ")," "))+4)')
            #Look for HOTPOINT in product title, with HBN appending the part code and extract the first three words (Part Code) from the span node
        #l.add_xpath('sku', 'substring(//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"HBN")],1,string-length(substring-before(//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"HBN")]," "))+string-length(substring-before(substring-after(//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"HBN")]," ")," "))+4)')
            #Look for HOTPOINT in product title, Extract everything between Hotpoint and Electric Oven
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"Electric Oven")]', re=r"(.*)(?=Electric Oven)")
            #Look for HOTPOINT in product title, Extract everything between Hotpoint and Tall Freezer
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"Tall Freezer")]', re=r"(.*)(?=Tall Frezzer)")
            #Look for HOTPOINT in product title, Extract everything between Hotpoint and Undercounter for Chest Freezer
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"Chest Freezer")]', re=r"(.*)(?=Chest Freezer)")
            #Look for HOTPOINT in product title, Extract everything between Hotpoint and Undercounter for K Undercounter Freezer
        #l.add_xpath('sku', '//span[starts-with(.,"HOTPOINT")]/following::span[contains(.,"Undercounter Freezer")]', re=r"(.*)(?=Undercounter Freezer)")
            #Look for HOTPOINT in product title, take first word (Part Code) from next span node
        #l.add_xpath('sku', 'substring(//span[starts-with(.,"HOTPOINT")]/following::span[1],1,string-length(substring-before(//span[starts-with(.,"HOTPOINT")]/following::span[1]," ")))')
            #Look for LEISURE in product title, check if the title contains Cookmaster. If it does extract the full title but then only take the 2nd word (Part Code) using Regex in Python
        l.add_xpath('sku', '//span[starts-with(.,"LEISURE")]/following::span[contains(.,"Cookmaster")]', re=r"^(?:[^\s]*\s){1}([^\s]*)")
            #Look for CANDY in product title, take first word (Part Code) from next span node
        l.add_xpath('sku', 'substring(//span[starts-with(.,"CANDY")]/following::span[1],1,string-length(substring-before(//span[starts-with(.,"CANDY")]/following::span[1]," ")))')
            #Look for SAGE in product title, take first word (Part Code) from next span node
        l.add_xpath('sku', 'substring(//span[starts-with(.,"SAGE")]/following::span[1],1,string-length(substring-before(//span[starts-with(.,"SAGE")]/following::span[1]," ")))')
            #Look for FLAVEL in product title, check if the title contains Milano. If it does extract the full title but then only take the 2nd word (Part Code) using Regex in Python
        l.add_xpath('sku', '//span[starts-with(.,"FLAVEL")]/following::span[contains(.,"Milano")]', re=r"^(?:[^\s]*\s){1}([^\s]*)")   
            #Look for RANGEMASTER in product title, check if the title contains Kitchener. If it does extract the full title but then only take the 2nd word (Part Code) using Regex in Python
        l.add_xpath('sku', '//span[starts-with(.,"RANGEMASTER")]/following::span[contains(.,"Kitchener")]', re=r"^(?:[^\s]*\s){1}([^\s]*)")   
            #Look for CANNON in product title, check if the title contains Carrick. If it does extract the full title but then only take the 2nd word (Part Code) using Regex in Python
        l.add_xpath('sku', '//span[starts-with(.,"CANNON")]/following::span[contains(.,"Carrick")]', re=r"^(?:[^\s]*\s){1}([^\s]*)")   
            #Look for HOOVER in product title, check if the title contains H-HOB. If it does extract the full title but then only take the 2nd word (Part Code) using Regex in Python
        l.add_xpath('sku', '//span[starts-with(.,"HOOVER")]/following::span[contains(.,"H-HOB")]', re=r"^(?:[^\s]*\s){1}([^\s]*)")  
            #Look for HOOVER in product title, check if the title contains H-HOOD. If it does extract the full title but then only take the 3rd word (Part Code) using Regex in Python
        l.add_xpath('sku', '//span[starts-with(.,"HOOVER")]/following::span[contains(.,"H-HOOD")]', re=r"^(?:[^\s]*\s){3}([^\s]*)")  
            #Look for HOOVER in product title, with HVN prefixing the part code and extract the first two words (Part Code) from the span node
        l.add_xpath('sku', 'substring(//span[starts-with(.,"HOOVER")]/following::span[contains(.,"HVN")],1,string-length(substring-before(//span[starts-with(.,"HOOVER")]/following::span[contains(.,"HVN")]," "))+string-length(substring-before(substring-after(//span[starts-with(.,"HOOVER")]/following::span[contains(.,"HVN")]," ")," "))+1)')
            #Look for HOOVER in product title, check if the title contains H-OVEN. If it does extract the full title but then only take the 2nd word (Part Code) using Regex in Python
        l.add_xpath('sku', '//span[starts-with(.,"HOOVER")]/following::span[contains(.,"H-OVEN")]', re=r"^(?:[^\s]*\s){2}([^\s]*)")   
            #Look for HOOVER in product title, check if the title contains AXI. If it does extract the full title but then only take the 2nd word (Part Code) using Regex in Python
        l.add_xpath('sku', '//span[starts-with(.,"HOOVER")]/following::span[contains(.,"AXI")]', re=r"^(?:[^\s]*\s){1}([^\s]*)")   
            #Look for MIELE in product title, Extract everything upto WS Tall Freezer
        l.add_xpath('sku', '//span[starts-with(.,"MIELE")]/following::span[contains(.,"WS Tall Freezer")]', re=r"(.*)(?=WS Tall Freezer)")

            #Laptop Brand Matching between () in Box Contents
        #l.add_xpath('sku', '//span[starts-with(.,"ALIENWARE")]/following::span[contains(.,"laptop")]//th[contains(.,"Box contents"]/following::td)', re=r"(?<=\()(.*?)(?=\))")
        #l.add_xpath('sku', '//span[starts-with(.,"Acer")]/following::span[contains(.,"laptop")]//th[contains(.,"Box contents"]/following::td)', re=r"(?<=\()(.*?)(?=\))")
        #l.add_xpath('sku', '//span[starts-with(.,"Dell")]/following::span[contains(.,"laptop")]//th[contains(.,"Box contents"]/following::td)', re=r"(?<=\()(.*?)(?=\))")
        #l.add_xpath('sku', '//span[starts-with(.,"Lenovo")]/following::span[contains(.,"laptop")]//th[contains(.,"Box contents"]/following::td)', re=r"(?<=\()(.*?)(?=\))")
        #l.add_xpath('sku', '//span[starts-with(.,"Asus")]/following::span[contains(.,"laptop")]//th[contains(.,"Box contents"]/following::td)', re=r"(?<=\()(.*?)(?=\))")
        #l.add_xpath('sku', '//span[starts-with(.,"HP")]/following::span[contains(.,"laptop")]//th[contains(.,"Box contents"]/following::td)', re=r"(?<=\()(.*?)(?=\))")
        #l.add_xpath('sku', '//span[starts-with(.,"Microsoft")]/following::span[contains(.,"laptop")]//th[contains(.,"Box contents"]/following::td)', re=r"(?<=\()(.*?)(?=\))")
        #l.add_xpath('sku', '//span[starts-with(.,"Samsung")]/following::span[contains(.,"laptop")]//th[contains(.,"Box contents"]/following::td)', re=r"(?<=\()(.*?)(?=\))")
        #l.add_xpath('sku', '//span[starts-with(.,"Avita")]/following::span[contains(.,"laptop")]//th[contains(.,"Box contents"]/following::td)', re=r"(?<=\()(.*?)(?=\))")
        #l.add_xpath('sku', '//span[starts-with(.,"LG")]/following::span[contains(.,"laptop")]//th[contains(.,"Box contents"]/following::td)', re=r"(?<=\()(.*?)(?=\))")
        #l.add_xpath('sku', '//span[starts-with(.,"Medion")]/following::span[contains(.,"laptop")]//th[contains(.,"Box contents"]/following::td)', re=r"(?<=\()(.*?)(?=\))")

            #Look for KITCHENAID in product title, Extract the second word as the part code when the second span contains Artisan
        l.add_xpath('sku', '//span[starts-with(.,"KITCHENAID")]/following::span[contains(.,"Artisan")]', re=r"^(?:[^\s]*\s){1}([^\s]*)")

            #If it has a flix media box that has rendered, can we take the MPN from there...
        l.add_xpath('sku', '//div[@class="flix-model-title"]/text()')
        l.add_xpath('sku', '//div[@class="flix-mpn-desc"]/text()')

            #CATCH-ALL For First Word in second node of title
        l.add_xpath('sku', '//*[@id="content"]//h1/span[2]', re=r"(?<=<span>)(?:[^\s]*\s){0}([^\s]*)")
        #l.add_xpath('sku', '//*[@id="content"]//h1/span[2]', re=r"^(?:[^\s]*\s){0}([^\s]*)")

            #Standard no-logic extracts:
        l.add_xpath('price', '//meta[@property="og:price:amount"]/@content')
        l.add_xpath('price', '//meta[@property="twitter:data1"]/@content')          
        l.add_xpath('price', '//div[@class="amounts"]/div/div/span/text()')
            #Regex to remove all whitespacing
        l.add_xpath('stock', '//div[@data-component="channels-panel"]//span[@data-name="AddToBasket"]/following::text()[1]', re=r"(\b.*)(!?\b)")
        l.add_xpath('stock', '//li[@id="delivery"]//text()', re=r"(\b.*)(!?\b)")
        l.add_xpath('stock', '//meta[@property="twitter:data2"]/@content', re=r"(\b.*)(!?\b)")
        l.add_xpath('stock', '//div[@class="oos oos-no-alt border space-b"]//i/@class')
        l.add_xpath('pcwb_product_code', '//p[@class="prd-code"]/text()')

        #Attribute Scraping Fields
        l.add_xpath('TelevisionDiagonalSize', '//table[@class="simpleTable"]//th[starts-with(.,"Screen size")]/following::td[1]/text()')
        l.add_xpath('TelevisionDisplayFormat', '//table[@class="simpleTable"]//th[starts-with(.,"Resolution")]/following::td[1]/text()')
        l.add_xpath('TelevisionType', '//table[@class="simpleTable"]//th[starts-with(.,"Screen technology")]/following::td[1]/text()')
        l.add_xpath('TVTunerDigitalTVTuner', '//table[@class="simpleTable"]//th[starts-with(.,"TV tuner")]/following::td[1]/text()')
        l.add_xpath('TelevisionHDR10', '//table[@class="simpleTable"]//th[starts-with(.,"HDR")]/following::td[1]/text()')
            
        # Administration Fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('useragent', self.settings.get('USER_AGENT'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return l.load_item()