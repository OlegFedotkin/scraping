import scrapy
from scrapy.http import HtmlResponse
from scraping.jobparser.items import JobparserItem
from scraping.jobparser.selectors import ITEM_SELECTORS_SJ, NAVIGATION_SELECTORS

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Python&geo%5Bt%5D%5B0%5D=4']

    def parse(self, response: HtmlResponse):
        item_urls = response.xpath(NAVIGATION_SELECTORS["parse_item_sj"]).getall()
        for link in item_urls:
            yield response.follow(link, callback=self.parse_item)

        next_page = response.xpath(NAVIGATION_SELECTORS['parse_sj']).get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_item(self, response: HtmlResponse):
        item = JobparserItem()
        for key, xpath in ITEM_SELECTORS_SJ.items():
            item[key] = response.xpath(xpath)

        item["title"] = item["title"].get()
        item["salary"] = item["salary"].getall()
        item["url"] = response.url

        yield item
