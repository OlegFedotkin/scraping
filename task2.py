import requests
import json
import os
from dotenv import load_dotenv

load_dotenv("./.env")
key = "apikey"
apikey = os.getenv(key, None)


def get_weather():

    cityname = input('Еnter the name of the city: ')

    url = f'http://api.openweathermap.org/data/2.5/weather?q={cityname}&appid={apikey}'
    responce = requests.get(url)
    data = json.loads(responce.text)

    return data['main']['temp'], data['weather'][0]['description']


print(get_weather())
