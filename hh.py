import requests
from bs4 import BeautifulSoup
import time
import json


vacancy = input("Enter vacancy: ")
page_count = int(input("Enter count of pages: "))

url_base = "https://hh.ru/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&text="

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def get_info(url_base, vacancy, page_count, headers):
    all_names = []
    for page_number in range(page_count):
        url = f"{url_base}{vacancy}&page={page_number}"
        response = requests.get(url, headers=headers)
        time.sleep(1)
        soup = BeautifulSoup(response.text, "html.parser")
        elements = soup.find_all(attrs={'class': 'vacancy-serp-item__row vacancy-serp-item__row_header'})

        info = parse_info(elements)

        if bool(info) == False:
            print('The pages are over')
            return all_names

        all_names.extend(info)

    return all_names

def parse_info(elements):
    all_info = []
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

        all_info.append(info)

    return all_info

save_result = get_info(url_base, vacancy, page_count, headers)

with open("result_list.json", "w") as write_f:
  json.dump(save_result, write_f)