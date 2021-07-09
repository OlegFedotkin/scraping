from pymongo import MongoClient

MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB = 'vacancies'
MONGO_COLLECTION = 'vacancies_collection'

def insert_into_mongo_db(vacancy):
    with MongoClient(MONGO_HOST, MONGO_PORT) as client:
        db = client[MONGO_DB]
        vacancies = db[MONGO_COLLECTION]
        vacancies.insert_one(vacancy)
