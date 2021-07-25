import scrapy

# useful for handling different item types with a single interface
from scrapy.pipelines.images import ImagesPipeline
import pymongo
from leroymerlin.settings import MONGO_HOST, MONGO_PORT
import hashlib
from scrapy.utils.python import to_bytes

class LeroymerlinImagesPipeline(ImagesPipeline):


    def get_media_requests(self, item, info):
        if item["img_urls"]:
            for img_link in item["img_urls"]:
                try:
                    yield scrapy.Request(img_link)

                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):

        if results:
            item["img_info"] = [x[1] for x in results if x[0]]
        if item["img_urls"]:
            del item["img_urls"]
        return item


    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        ware_name = item['url'].split('/')
        ware_name = ware_name[-2]

        return f'{ware_name}/{image_guid}.jpg'


class LeroymerlinPipeline:

    def __init__(self):
        self.client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
        self.db = self.client.leroymerlin

    def process_item(self, item, spider):

        title_value = item.get('name')
        link_value = item.get('url')
        price = item.get('price')
        img_urls = item.get('img_urls')
        specification = item.get('specification')
        img_info = item.get('specification')

        key = {'name': title_value}
        data = {'$set':
                    {'url': link_value,
                     'price': price,
                     'img_urls': img_urls,
                    'specification': specification,
                     'img_info': img_info}
        }


        self.db[spider.name].update_one(key, data, upsert=True)

        # self.db[spider.name].insert_one(item)
        return item
