from pymongo import MongoClient

MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB = 'vacancies'
MONGO_COLLECTION = 'vacancies_collection'

def upsert_new_vacancies(info):
    vacancy_get = info.get('vacancy')
    link_get = info.get('link')
    compensation_min_get = info.get('compensation_min')
    compensation_max_get = info.get('compensation_max')
    comp_currency_get = info.get('comp_currency')

    key = {'link': link_get}
    data = {'$set':
                {'vacancy': vacancy_get,
                 'compensation_min': compensation_min_get,
                 'compensation_max': compensation_max_get,
                 'comp_currency': comp_currency_get}
            }

    with MongoClient(MONGO_HOST, MONGO_PORT) as client:
        db = client[MONGO_DB]
        vacancies = db[MONGO_COLLECTION]
        vacancies.update_one(key, data, upsert=True)
