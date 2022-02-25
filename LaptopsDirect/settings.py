# -*- coding: utf-8 -*-

# Available Settings:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

#Used for tracking what is running on the cloud provider and identifying the settings taken if there are multiple setting files in play
BOT_NAME = 'T-1000'

#Ties these settings into this batch of spiders
SPIDER_MODULES = ['LaptopsDirect.spiders']
NEWSPIDER_MODULE = 'LaptopsDirect.spiders'

#How the spider reports itself to the website being browsed. If it gets too out of date people start blocking it
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'

# Obey robots.txt rules. **DO NOT REMOVE THIS AS IS REQUIRED FOR CLOUD PROVIDER T&Cs**
ROBOTSTXT_OBEY = True

# Try to make the spider less predictable
RANDOMIZE_DOWNLOAD_DELAY = True
DOWNLOAD_DELAY = 0.10

# Seems to work best?
COOKIES_ENABLED = False

#Needed for Very Testing
#DEFAULT_REQUEST_HEADERS = {
   # 'Referer': 'https://www.google.com' 
#}

# Autothrottle Settings
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5.0
AUTOTHROTTLE_MAX_DELAY = 60.0
AUTOTHROTTLE_TARGET_CONCURRENCY = 8.0
AUTOTHROTTLE_DEBUG = False

#Reduce this number to a small amount for testing spiders. Large number stops a spider running into infinity and the other pagecount or errorcount closespiders were not set
CLOSESPIDER_ITEMCOUNT = 10000000

#Used to cull a bad spider that is stuck on a site, rather than it going to infinity. Largest number of requests on a spider at time of implimentation was 50k
CLOSESPIDER_PAGECOUNT = 300000
CLOSESPIDER_ERRORCOUNT = 75
CLOSESPIDER_TIMEOUT = 86400

#Rotating list of user agents used by select spiders
#USER_AGENTS = [
#    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
#    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
#    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
#    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
#    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134',
#    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763',
#    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36',
#    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
#    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
#    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
#    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36',
#    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
#    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
#    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'

#]

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'LaptopsDirect.middlewares.LaptopsdirectSpiderMiddleware': 543,
#}

# Enable or disable spider middlewares - Brandon Added
#See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
    #'LaptopsDirect.middlewares.httperror.HttpErrorMiddleware' : 420
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'LaptopsDirect.middlewares.RotateUserAgentMiddleware': 110,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'scrapy.pipelines.images.ImagesPipeline': 1,
}

#Store for the images, local storage use this path. If no drive letter is configured for execution on Debian based Linux. Can be configured for Amazon S3 storage or a FTP
IMAGES_STORE = 'images'

#Media pipelines ignore redirects, i.e. an HTTP redirection to a media file URL request will mean the media download is considered failed. This fixes that.
MEDIA_ALLOW_REDIRECTS = True

#Path for FTP feed export on home deployment
#FEED_URI="ftp://epiz_23613572:Y7XpLLh2XzhJL@ftpupload.net/feeds/scan.csv"

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# Also DBM might be required: https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#dbm-storage-backend 
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

#Log the duplicates being found, rather than just the first instance. Used to show activity when some of the spiders just pause for ages after loading a sitemap and if a xpath rule needs additing to filter results.
DUPEFILTER_DEBUG = True

#List of rotating proxies for the proxy rotator middleware
ROTATING_PROXY_LIST = [
        '104.248.169.218:8118', '176.248.120.70:3128', '46.101.50.133:8080', '51.158.172.165:8811', '51.158.165.18:8811',
        '78.141.222.210:8080', '78.141.211.143:8080', '167.172.180.46:42580', '167.172.184.166:43827', '51.77.144.148:3128',
        '167.172.180.40:34265', '51.158.165.18:8811', '51.158.165.18:8811', '163.172.47.182:8080', '167.172.184.166:40607',
        '167.172.180.46:35884', '51.158.186.242:8811', '51.158.172.165:8811', '167.172.180.46:37121', '159.65.69.186:9300', 
        '194.35.233.128:89'
    ]