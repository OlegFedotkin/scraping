# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Compose, MapCompose, TakeFirst


def clean_name(string_array):
    return " ".join(map(lambda x: x.strip(), string_array)).strip()


def clean_string(s):
    return int(s.strip().replace(' ', ''))


def clean_specification(s):
    s = map(lambda x: x.strip(), s)
    s = [value for value in s if value]
    s = {s[i]: s[i + 1] for i in range(0, len(s), 2)}
    return s


class LeroymerlinItem(scrapy.Item):

    url = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(
        input_processor=Compose(clean_name), output_processor=TakeFirst()
    )
    price = scrapy.Field(input_processor=MapCompose(clean_string), output_processor=TakeFirst())
    img_urls = scrapy.Field()
    specification = scrapy.Field(input_processor=Compose(clean_specification))
    # specification_value = scrapy.Field()
    img_info = scrapy.Field()
    _id = scrapy.Field()

