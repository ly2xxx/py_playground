from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
#scrapy crawl scrapeme --logfile scrapeme.log
class ImdbCrawler(CrawlSpider):
    name = 'scrapeme'
    allowed_domains = ['scrapeme.live']
    start_urls = ['https://scrapeme.live/shop/']
    rules = (Rule(LinkExtractor()),)