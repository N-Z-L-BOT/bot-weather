import locale
from datetime import datetime
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


def emoticon_description(state: str) -> str:
    '''

    :param state: описание погоды от OpenWeather
    :return: возвращает смайлик (описание погоды)
    '''
    supplementary_data = ('Mist', 'Smoke', 'Haze', 'Dust', 'Fog', 'Sand', 'Dust', 'Ash', 'Squall', 'Tornado')

    exist_weather = {
        'Clear': "\U00002600",
        'Thunderstorm': '\U0001F329',
        'Drizzle': '\U0001F326',
        'Rain': '\U0001F327',
        'Snow': '\U00002744',
        'Clouds': '\U00002601'
    }
    result = exist_weather.get(state.capitalize())
    if result:
        return result

    elif result is None and state in supplementary_data:
        return '\U0001F32A'

    return '\U0001F300'


def get_beautiful_date_and_time(day_and_time=None) -> tuple[str, str]:
    '''

    :param day_and_time: получает дату или None
    :return: возвращает красивый для пользователя вид даты и времени
    '''
    if day_and_time is None:
        date = datetime.now()
        date_answer = date.strftime('%A %d, %B %Y')
        time_answer = date.strftime('%H:%M:%S')

    else:
        full_date = datetime.strptime(day_and_time, '%Y-%m-%d %H:%M:%S')
        date_answer = full_date.strftime('%A %d, %B %Y')
        time_answer = full_date.strftime('%H:%M:%S')

    return date_answer, time_answer


def clear_excess_sym(data: list[str]) -> tuple[str]:
    '''

    :param data: получает данные с городами
    :return: чистит список от возможной некорректной работы метода split
    '''
    if '' in data:
        return tuple(town for town in data if town != '')
    return tuple(data)


def generate_answer(condition: bool, params: str) -> str:
    '''

    :param condition: булево значение
    :param params: описание того, что нужно искать
    :return: возвращет параметр для ответа пользователю
    '''
    if condition and params == 'temp':
        return 'Параметр: самая высокая температура\n\n'
    elif condition is False and params == 'temp':
        return 'Параметр: самая низкая температура\n\n'
    elif condition and params == 'duration':
        return 'Параметр: самая максимальная продолжительность дня\n\n'
    elif condition is False and params == 'duration':
        return 'Параметр: самая минимальная продолжительность дня\n\n'


def result(full_data: list, params: str) -> str:
    '''

    :param full_data: список городов и описаний погоды
    :param params: описание того, что нужно искать
    :return: возвращает аналитику для ответа пользователю
    '''
    answer = str()
    if full_data and params == 'temp':
        count = 1
        for town, state, like in full_data:
            answer += f'{count}) {town}: {state}°C (ощущается, как {like}°C)\n'
            count += 1

    elif full_data and params == 'duration':
        count = 1
        for town, during in full_data:
            answer += f'{count}) {town}: {during}\n'
            count += 1
    return answer


def mistake(mistake_query: list, date: str, time: str):
    '''

    :param mistake_query: список городов, которых не удалось найти
    :param date: дата ответа
    :param time: время ответа
    :return: возвращает ошибки в ответ пользователю
    '''
    answer = str()
    if mistake_query:
        answer += '\nИнформация не найдена по городам:\n'
        for miss in mistake_query:
            answer += f'- {miss}\n'

    answer += f'\nДата ответа: {date} {time}'
    return answer


def descriptions(info: list[dict]) -> str:
    '''

    :param info: получает структуру от OpenWeather
    :return: возвращет описание и смайлик к этому описанию
    '''
    return info[0].get('description') + emoticon_description(info[0].get('main'))


def get_data_about_weather(data: dict, name_town: str, date_predict: str, time_predict: str, sunrise: datetime,
                           sunset: datetime, date_answer: str, time_answer: str) -> str:
    '''

    :param data: словарь с данными
    :param name_town: название города
    :param date_predict: дата прогноза
    :param time_predict: время прогноза
    :param sunrise: время рассвета
    :param sunset: время заката
    :param date_answer: дата ответа
    :param time_answer: время ответа
    :return: возвращает полную аналитику погоды
    '''

    error_data = 'Информация не найдена'
    description = descriptions(data.get('weather', error_data))
    current_temp = data.get('main').get('temp', error_data)
    feels_temp = data.get('main').get('feels_like', error_data)
    pressure = data.get('main').get('pressure', error_data)
    humidity = data.get('main').get('humidity', error_data)
    speed_winter = data.get('wind').get('speed', error_data)
    level_sea = data.get('main').get('sea_level', error_data)
    duration_day = sunset - sunrise

    answer = f"Прогноз на {date_predict} {time_predict}:\n\n" \
             f"Название города: {name_town}\n" \
             f"Краткое описание: {description}\n" \
             f"Текущая температура: {current_temp}°C (ощущается, как {feels_temp}°C)\n" \
             f"Давление: {pressure} мм рт. ст.\n" \
             f"Влажность: {humidity} г/м^3\n" \
             f"Скорость ветра: {speed_winter} м/с💨\n" \
             f"Восход солнца: {sunrise}🌞\n" \
             f"Закат солнца: {sunset}\U0001F311\n" \
             f"Продолжительность дня: {duration_day}\n" \
             f"Уровень моря: {level_sea}🌊\n\n" \
             f"Дата ответа: {date_answer}. Время ответа: {time_answer}"

    return answer


def error_load(date_predict: str, time_predict: str, date_answer: str, time_answer: str, city: str) -> str:
    '''

    :param date_predict: дата прогноза
    :param time_predict: время прогноза
    :param date_answer: дата ответа
    :param time_answer: время ответа
    :param city: название города
    :return: возвращает ошибку
    '''
    return f'Прогноз на {date_predict} {time_predict}:\n\nК сожалению, не удалось найти информацию о городе {city}.\n' \
           f'Попробуйте позже или введите другой запрос.\nДата ответа: {date_answer} {time_answer}.'


def statistic(data_scores: list, user_score: int) -> int:
    '''

    :param data_scores: список со всеми очками OpenWeather всех юзеров
    :param user_score: очки конкретного юзера
    :return: возвращет процент того, насколько результат строго больше, чем результаты других юзеров
    '''
    if user_score == (0,):
        return 0

    len_data_scores = len(data_scores) - 1
    if len_data_scores == 0:
        return 100

    return int((sorted(data_scores).index((user_score,))) / len_data_scores * 100)












