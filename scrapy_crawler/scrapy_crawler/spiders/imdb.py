from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
#scrapy crawl imdb --logfile imdb.log
class ImdbCrawler(CrawlSpider):
    name = 'imdb'
    allowed_domains = ['www.imdb.com']
    start_urls = ['https://www.imdb.com/']
    rules = (Rule(LinkExtractor()),)