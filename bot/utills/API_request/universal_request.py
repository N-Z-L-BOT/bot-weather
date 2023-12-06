import requests
from loader import OPENWEATHER_API_KEY
import json


def make_request(city: str, method: str) -> dict | None:
    '''

    :param city: название города
    :param method: метод для запроса к апи
    :return: возвращает либо словарь, либо None, если был неудачный запрос к OpenWeather
    '''
    params = {'q': city, 'appid': OPENWEATHER_API_KEY, 'units': 'metric', 'lang': 'ru'}
    link = f'https://api.openweathermap.org/data/2.5/{method}'
    try:
        response = requests.get(link, params=params)
        if response:
            try:
                data = json.loads(response.text)
                return data
            except Exception:
                return None
        return None

    except Exception:
        return None