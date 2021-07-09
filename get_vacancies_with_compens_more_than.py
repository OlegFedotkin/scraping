from pymongo import MongoClient


MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB = 'vacancies'
MONGO_COLLECTION = 'vacancies_collection'

compensation = int(input("Enter compensation: "))

def get_vacancies_with_compens_more_than(MONGO_HOST, MONGO_PORT, MONGO_DB, MONGO_COLLECTION, compensation):
    with MongoClient(MONGO_HOST, MONGO_PORT) as client:
        db = client[MONGO_DB]
        vacancies = db[MONGO_COLLECTION]
        vacancies_with_compens_more_than = vacancies.find({
            'compensation_min': {'$gt': compensation}
        })
    return vacancies_with_compens_more_than
