from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from scraping.jobparser.spiders.sjru import SjruSpider
from scraping.jobparser import settings
from scraping.jobparser.spiders.hhru import HhruSpider

if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhruSpider)
    process.crawl(SjruSpider)

    process.start()