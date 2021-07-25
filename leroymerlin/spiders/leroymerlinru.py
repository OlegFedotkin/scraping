import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader

from leroymerlin.items import LeroymerlinItem



class LeroymerlinruSpider(scrapy.Spider):
    name = 'leroymerlinru'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['http://leroymerlin.ru/']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f"https://leroymerlin.ru/search/?q=дрели"]

    def parse(self, response: HtmlResponse, **kwargs):
        links = response.xpath('//div[contains(@class, "largeCard") and (@data-qa-product)]/a/@href')
        for link in links:
            yield response.follow(link, callback=self.parse_item)

        next_page = response.xpath('//div[@role="navigation"]//a[@data-qa-pagination-item="right"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)


    def parse_item(self, response: HtmlResponse):
        # get only the first element with this xpath
        price_xpath = '//span[contains(@slot, "price")]//text()'
        name_xpath = "//h1//text()"
        image_xpath = '//div[contains(@class, "detailed-view-inner container")]//img/@src'
        specification_xpath = '//div[contains(@class, "def-list__group")]//text()'
        # specification_value_xpath = '//div[contains(@class, "def-list__group")]/dd//text()'

        loader = ItemLoader(item=LeroymerlinItem(), response=response)
        loader.add_value("url", response.url)
        loader.add_xpath("name", name_xpath)
        loader.add_xpath("price", price_xpath)
        loader.add_xpath("img_urls", image_xpath)
        loader.add_xpath("specification", specification_xpath)
        # loader.add_xpath("specification_value", specification_value_xpath)

        yield loader.load_item()
