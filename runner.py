from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from leroymerlin import settings
from leroymerlin.spiders.leroymerlinru import LeroymerlinruSpider

from urllib.parse import quote_plus


if __name__ == "__main__":
    custom_settings = Settings()
    custom_settings.setmodule(settings)

    query = quote_plus("дрели".encode(encoding='utf-8'))

    process = CrawlerProcess(settings=custom_settings)
    process.crawl(LeroymerlinruSpider)

    process.start()