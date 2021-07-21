# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
from scraping.jobparser.settings import MONGO_HOST, MONGO_PORT


class JobparserPipeline:
    def __init__(self):
        self.client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
        self.db = self.client.vacancies

    # TODO: implement this
    def process_salary(self, salary):
        salary = salary[0].replace('\xa0', '').split(' ')
        if salary[0] == 'до':
            salary_min = None
            salary_max = int(salary[1])
            currency = salary[2][0:3]
        elif salary[2] == 'до':
            salary_min = int(salary[1])
            salary_max = int(salary[3])
            currency = salary[4][0:3]
        elif salary[1] == 'не':
            salary_min = None
            salary_max = None
            currency = None
        else:
            salary_min = int(salary[1])
            salary_max = None
            currency = salary[2][0:3]

        return salary_min, salary_max, currency


    def process_salary_sj(self, salary):
        if salary[0] == 'от':
            salary = salary[2].replace('\xa0', '')
            salary_min = int(salary[:-4].replace('\xa0', ''))
            salary_max = None
            currency = salary[-4:]
        elif salary[0] == 'до':
            salary = salary[2].replace('\xa0', '')
            salary_min = None
            salary_max = int(salary[:-4].replace('\xa0', ''))
            currency = salary[-4:]
        elif not salary[0]:
            salary_min = None
            salary_max = None
            currency = None
        else:
            salary_min = int(salary[0].replace('\xa0', ''))
            salary_max = int(salary[4].replace('\xa0', ''))
            currency = salary[6]

        return salary_min, salary_max, currency


    def process_item(self, item, spider):

        if spider.name == 'hhru':
            s_min, s_max, currency = self.process_salary(item["salary"])
        else:
            s_min, s_max, currency = self.process_salary_sj(item["salary"])

        item['salary_min'], item['salary_max'], item['currency'] = s_min, s_max, currency

        del item["salary"]

        item["source"] = spider.name

        print(item)

        title_value = item.get('title')
        link_value = item.get('url')
        salary_min_value = item.get('salary_min')
        salary_max_value = item.get('salary_max')
        currency_value = item.get('currency')
        source_value = item.get('source')

        key = {'url': link_value}
        data = {'$set':
                    {'title': title_value,
                     'salary_min': salary_min_value,
                     'salary_max': salary_max_value,
                     'currency': currency_value,
                    'source': source_value}
        }


        self.db['hh_sj'].update_one(key, data, upsert=True)

        return item

    def close_spider(self):
        self.client.close()
