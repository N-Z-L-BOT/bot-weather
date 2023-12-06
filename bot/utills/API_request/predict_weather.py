from utills.API_request.universal_request import make_request
from utills.beautiful_print import get_beautiful_date_and_time, generate_answer, result, mistake,\
    get_data_about_weather, error_load

from datetime import datetime


def select_day(data: dict, period: str) -> dict | None:
    '''

    :param data: полный словарь от OpenWeather
    :param period: нужный юзеру период
    :return: маленький словарь с конкретным периодом или None
    '''
    all_days: list[dict] = data.get('list')
    for day in all_days:
        if day.get('dt_txt') == period:
            return day
    else:
        return None


def predict_analytics_weather(city: str, period: str, method: str = 'forecast') -> str:
    '''

    :param city: название города
    :param period: период времени
    :param method: метод для запроса к апи
    :return: возвращет результат функции get_data_about_weather(ответ пользователю)
    '''
    common_data = make_request(city, method)
    date, time = get_beautiful_date_and_time()
    date_search_period, time_search_period = get_beautiful_date_and_time(period)
    if common_data is None:
        return error_load(date_predict=date_search_period, time_predict=time_search_period, date_answer=date,
                          time_answer=time, city=city)

    data = select_day(data=common_data, period=period)

    if data is None:
        return error_load(date_predict=date_search_period, time_predict=time_search_period, date_answer=date,
                          time_answer=time, city=city)

    sunrise = datetime.fromtimestamp(common_data.get('city').get('sunrise'))
    sunset = datetime.fromtimestamp(common_data.get('city').get('sunset'))

    return get_data_about_weather(data=data, date_predict=date_search_period, time_predict=time_search_period,
                                  date_answer=date, time_answer=time, name_town=city, sunrise=sunrise, sunset=sunset)


def select_top_towns_predict(cities: tuple, period: str, params: str, condition: bool, method: str = 'forecast') -> str:
    '''

    :param cities: кортеж с городами
    :param period: нужный период
    :param params: параметр для поиска
    :param condition: аргумент для сортировки
    :param method: метод для запроса к апи
    :return: возвращает ответ пользователю
    '''
    mistake_query = []
    full_data = []
    date, time = get_beautiful_date_and_time()
    date_search_period, time_search_period = get_beautiful_date_and_time(period)

    for city in cities:
        common_data = make_request(city, method)
        if common_data is None:
            mistake_query.append(city)

        else:
            data = select_day(data=common_data, period=period)
            if data is None:
                mistake_query.append(city)

            else:
                if params == 'duration':
                    full_data.append((city, datetime.fromtimestamp(common_data.get('city').get('sunset')) - datetime.fromtimestamp(common_data.get('city').get('sunrise'))))

                elif params == 'temp':
                    full_data.append((city, data.get('main').get('temp'), data.get('main').get('feels_like')))

    full_data.sort(key=lambda x: x[1], reverse=condition)
    answer = f'Прогноз на {date_search_period} {time_search_period}\n'
    answer += generate_answer(condition=condition, params=params)
    answer += result(full_data=full_data, params=params)
    answer += mistake(mistake_query=mistake_query, date=date, time=time)

    return answer




