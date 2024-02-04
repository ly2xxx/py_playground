from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
#scrapy crawl amazon --logfile amazon_warehouse.log
class ImdbCrawler(CrawlSpider):
    name = 'amazon'
    allowed_domains = ['www.amazon.co.uk']
    start_urls = ['https://www.amazon.co.uk/s?k=ddr4+ram+32gb&i=warehouse-deals&crid=2OPZW6GTCC5QG&sprefix=ddr4%2Cwarehouse-deals%2C127&ref=nb_sb_ss_ts-doa-p_3_4']
    rules = (Rule(LinkExtractor()),)