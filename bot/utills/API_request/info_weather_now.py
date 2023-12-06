from datetime import datetime
from utills.beautiful_print import get_beautiful_date_and_time, generate_answer, result, mistake,\
    get_data_about_weather, error_load
from utills.API_request.universal_request import make_request


def analytics_weather(city: str, method) -> str:
    '''

    :param city: название города
    :param method: метод для запроса
    :return: возвращет результат функции get_data_about_weather(ответ пользователю)
    '''
    data = make_request(city, method)
    date, time = get_beautiful_date_and_time()
    if data is None:
        return error_load(date_answer=date, time_answer=time, city=city, date_predict=date, time_predict=time)

    sunrise = datetime.fromtimestamp(data.get('sys').get('sunrise'))
    sunset = datetime.fromtimestamp(data.get('sys').get('sunset'))
    return get_data_about_weather(data=data, name_town=city, date_predict=date, time_predict=time, sunrise=sunrise,
                                  sunset=sunset, date_answer=date, time_answer=time)


def select_top_towns_now(cities: tuple, params: str, condition: bool, method: str = 'weather') -> str:
    '''

    :param cities: кортеж с городами
    :param params: параметр для поиска
    :param condition: аргумент для сортировки
    :param method: метод для запроса
    :return: возвращает ответ пользователю
    '''
    mistake_query = []
    full_data = []
    date, time = get_beautiful_date_and_time()
    for city in cities:
        data = make_request(city, method)
        if data is None:
            mistake_query.append(city)

        else:
            if params == 'duration':
                full_data.append((city, datetime.fromtimestamp(data.get('sys').get('sunset')) - datetime.fromtimestamp(data.get('sys').get('sunrise'))))

            elif params == 'temp':
                full_data.append((city, data.get('main').get('temp'), data.get('main').get('feels_like')))

    full_data.sort(key=lambda x: x[1], reverse=condition)
    answer = f'Прогноз на {date} {time}\n'
    answer += generate_answer(condition=condition, params=params)
    answer += result(full_data=full_data, params=params)
    answer += mistake(mistake_query=mistake_query, date=date, time=time)

    return answer








