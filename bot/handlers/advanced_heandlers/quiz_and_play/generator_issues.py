import random


def security_issues() -> tuple:
    '''

    :return: возвращает вопросы
    '''
    return ({'Наука изучающая воздушную оболочку:': ('А) ПОГОДОЛОГИЯ Б) МЕЗОСФЕРОЛОГИЯ В) МЕТЕРОЛОГИЯ', 'В')},
            {
                'Самая высокая температура на Земле, составляющая 57,8 °C, была зарегистрирована в городе Тират-Цви в Израиле, так ли это?':
                    ('А) ДА Б) НЕТ В) НЕИЗВЕСТНО', 'Б')},
            {'Повышение температуры на Земле, связанное с деятельностью человека:': (
            'А) ГЛОБАЛЬНОЕ ПОТЕПЛЕНИЕ Б) ГЛОБАЛЬНОЕ ПОХОЛОДНЕНИЕ В) ВСЕМИРНЫЙ ПОТОП', 'А')},
            {'Бриз и шторм – распространённые термины, которые используются для описания скорости чего:': (
            'а) Воды б) Ветра в) Схода лавины', 'б')},
            {
                'Радуга – это световой спектр, который появляется, когда солнце подсвечивает капельки воды в воздухе, так ли это:': (
                'а) Нет б) Да в) Неизвестно', 'б')},
            {'В какой стране появляется наибольшее количество торнадо?': ('а) Россия б) США в) Бразилия', 'б')},
            {'Дождевые, кучевые, перистые, слоистые. Что имеется в виду?': ('а) Туманы б) Дожди в) Облака', 'в')},
            {'Центры наблюдения за погодой:': ('а) Лаборатории б) Метеостанции в) Оба варианта ответа верны', 'б')},
            {'Самая сухая пустыня на Земле': ('а) Сахара б) Атакама, в) Калахари', 'б')},
            {'Во время лавины происходит быстрый спуск': ('а) Воды б) Снега в) Льда', 'б')})


def get_question_and_responses_and_right(index: int) -> tuple[str, str, str]:
    '''

    :param index: номер вопроса
    :return: возвращает вопрос, варианты ответа и правильный ответ
    '''
    full_issues = security_issues()
    data_issue = full_issues[index]
    text_question = tuple(data_issue.keys())[0]
    variants = data_issue[text_question][0]
    right_response = data_issue[text_question][1]
    return text_question, variants, right_response


def count_right_response(data: dict) -> tuple[str, int]:
    '''

    :param data: принимает данные
    :return: возвращает ответ и количество правильных ответов
    '''
    dict_transform = {True: 'Верно.', False: 'Неверно.'}
    full_responses = (data.get('response1'), data.get('response2'), data.get('response3'))
    outcome1 = dict_transform[full_responses[0]]
    outcome2 = dict_transform[full_responses[1]]
    outcome3 = dict_transform[full_responses[2]]
    total = sum(full_responses) * random.randint(3, 8)
    answer = f'Первый вопрос:  {outcome1}\nВторой вопрос:  {outcome2}\nТретий вопрос:  {outcome3}\n' \
             f'Получено очков OpenWeather: {total}\n' \
             f'Возвращайтесь снова!'
    return answer, total


