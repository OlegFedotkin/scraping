import requests
from bs4 import BeautifulSoup
import time
from pymongo import MongoClient


MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB = 'vacancies'
MONGO_COLLECTION = 'vacancies_collection'

vacancy = input("Enter vacancy: ")
page_count = int(input("Enter count of pages: "))

url_base = "https://hh.ru/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&text="

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def get_info(url_base, vacancy, page_count, headers):
    # all_names = []
    for page_number in range(page_count):
        url = f"{url_base}{vacancy}&page={page_number}"
        response = requests.get(url, headers=headers)
        time.sleep(1)
        soup = BeautifulSoup(response.text, "html.parser")
        elements = soup.find_all(attrs={'class': 'vacancy-serp-item__row vacancy-serp-item__row_header'})

        parse_info(elements)


def parse_info(elements):
    for elem in elements:
        info = {}
        element = elem.find(attrs={'class': 'bloko-link', 'data-qa': "vacancy-serp__vacancy-title"})
        info['vacancy'] = element.text
        link = element.get('href').split('?')
        info['link'] = link[0]
        website = element.get('href').split('/')
        info['website'] = website[2]
        try:
            compensation = elem.find('span', attrs={'data-qa': "vacancy-serp__vacancy-compensation"}).text
            if compensation.startswith('от'):
                compensation_split = compensation.split(' ')
                info['compensation_min'] = int(compensation_split[1].replace('\u202f', ''))
                info['compensation_max'] = None
                info['compensation_currency'] = compensation_split[2]
            elif compensation.startswith('до'):
                compensation_split = compensation.split(' ')
                info['compensation_min'] = None
                info['compensation_max'] = int(compensation_split[1].replace('\u202f', ''))
                info['compensation_currency'] = compensation_split[2]
            else:
                compensation_split = compensation.split(' ')
                info['compensation_min'] = int(compensation_split[0].replace('\u202f', ''))
                info['compensation_max'] = int(compensation_split[2].replace('\u202f', ''))
                info['comp_currency'] = compensation_split[3]
        except AttributeError as all:
            info['compensation_min'] = None
            info['compensation_max'] = None
            info['compensation_currency'] = None
        except TypeError as t:
            info['compensation_min'] = None
            info['compensation_max'] = None
            info['compensation_currency'] = None

        insert_into_mongo_db(info)   # Заполнение базы собранными вакансиями
        # upsert_new_vacancies(info) # Добавление в базу только новых вакансий


def insert_into_mongo_db(vacancy):
    with MongoClient(MONGO_HOST, MONGO_PORT) as client:
        db = client[MONGO_DB]
        vacancies = db[MONGO_COLLECTION]
        vacancies.insert_one(vacancy)


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


get_info(url_base, vacancy, page_count, headers)
