from scrapy.crawler import CrawlerProcess
from LaptopsDirect import settings
from LaptopsDirect.spiders import AO, AOCrawler
from scrapy.utils.project import get_project_settings

Spider1 = AO.AoSpider.parse
Spider2 = AOCrawler.AOCrawlSpider.parse_item

process = CrawlerProcess(get_project_settings())
process.crawl(Spider1)
process.crawl(Spider2)
process.start()