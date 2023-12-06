import locale
from datetime import datetime, timedelta, date
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


def get_5_date() -> dict[str]:
    '''

    :return: возвращает словарь с валидными "красивыми" и ISO - датами
    '''
    start_datetime = datetime.now()
    start_date = date(year=start_datetime.year, month=start_datetime.month, day=start_datetime.day)
    full_date = tuple(str(start_date + timedelta(n)) for n in range(6))

    main_dict = {'Сегодня': full_date[0]}
    intermediate_dict = {datetime.strptime(day, '%Y-%m-%d').strftime('%A %d, %B %Y'): day for day in full_date[1:]}

    return main_dict | intermediate_dict


full_date: dict[str] = get_5_date()


def treat_time(n: int) -> str:
    '''

    :param n: принимает час
    :return: возвращает красивый вид времени
    '''
    if n < 10:
        return f'0{n}:00:00'
    return f'{n}:00:00'


def get_valid_time(now: bool) -> tuple[str] | None:
    '''

    :param now: True - если пользователю нужно время сегодняшнее время, False - любое времмя
    :return: возвращает либо кортеж со временем, либо None для дальнейшей обработки
    '''
    full_time = (0, 3, 6, 9, 12, 15, 18, 21)
    if now:
        current_hour = datetime.now().hour
        full_time = (0, 3, 6, 9, 12, 15, 18, 21)
        for index, hour in enumerate(full_time):
            if hour > current_hour:
                return tuple(map(treat_time, full_time[index - 1:]))

            if hour == current_hour:
                return tuple(map(treat_time, full_time[index:]))
        else:
            return None

    else:
        return tuple(map(treat_time, full_time[:]))












