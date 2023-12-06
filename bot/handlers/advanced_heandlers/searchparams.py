from loader import bot
from telebot.types import Message
from states.information_city_state import CorrectRequestHighAndLowParams
from database.information_users_DB import DataUsers
from database.data_on_requests_and_responses_DB import HistoryDB
from keyboards.reply.set_time_and_calendar_keyboard import set_time_now, set_time, set_date
from utills.date_and_time import full_date, get_valid_time
from utills.API_request.predict_weather import select_top_towns_predict
from keyboards.reply.defoult_keboard import buttons_for_help, button_for_back, button_for_survey
from states.user_state_survey import back
from utills.beautiful_print import clear_excess_sym
from keyboards.reply.advanced_keyboard import choice_params, sort_keyboard
from utills.API_request.info_weather_now import select_top_towns_now

@bot.message_handler(commands=['searchparams'])
def high_temperature(message: Message) -> None:
    '''
    запрашивает города

    :param message: сообщение юзера
    :return:
    '''
    USER = DataUsers()
    if USER.exist_user(message.from_user.id):
        bot.set_state(message.from_user.id, CorrectRequestHighAndLowParams.cities, message.chat.id)
        bot.send_message(message.from_user.id, 'Введите интересующие города через запятую и пробел(минимум 2 города, максимум 10). \n'
                                               'Пример ввода: Москва, Волгоград, Сочи', reply_markup=button_for_back())
    else:
        bot.send_message(message.from_user.id, 'Пожалуйста, пройдите опрос /survey.', reply_markup=button_for_survey())


@bot.message_handler(state=CorrectRequestHighAndLowParams.cities)
def get_cities(message: Message) -> None:
    '''
    проверяет ввод, запрашивает параметр

    :param message: сообщение юзера
    :return:
    '''
    if back(message):
        if all((not(letter.isdigit())) for letter in message.text):
            treatment = clear_excess_sym(message.text.split(', '))
            if len(treatment) < 2 or len(treatment) > 10:
                bot.send_message(message.from_user.id, 'Нужно выбрать минимум два города, максимум 10.'
                                                       ' Перепроверьте корректность запроса и попробуйте снова.',
                                 reply_markup=button_for_back())

            else:
                with bot.retrieve_data(message.from_user.id, message.chat.id) as data_user:
                    data_user['cities'] = treatment
                bot.set_state(message.from_user.id, CorrectRequestHighAndLowParams.params, message.chat.id)
                bot.send_message(message.from_user.id, 'Теперь выберете нужный параметр для поиска.', reply_markup=choice_params())

        else:
            bot.send_message(message.from_user.id, 'Города не содержат цифр. Попробуйте снова.\n'
                                                   'Пример ввода: Москва, Волгоград, Сочи', reply_markup=button_for_back())


@bot.message_handler(state=CorrectRequestHighAndLowParams.params, content_types=['text'])
def get_params(message: Message) -> None:
    '''
    получает параметр и запрашивает вид сортировки

    :param message: сообщение юзера
    :return:
    '''
    if back(message):
        if message.text == 'Температура':
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data_user:
                data_user['params'] = 'temp'
            bot.set_state(message.from_user.id, CorrectRequestHighAndLowParams.terms, message.chat.id)
            bot.send_message(message.from_user.id, 'Выберете вид сортировки.', reply_markup=sort_keyboard())

        elif message.text == 'Продолжительность дня':
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data_user:
                data_user['params'] = 'duration'
            bot.set_state(message.from_user.id, CorrectRequestHighAndLowParams.terms, message.chat.id)
            bot.send_message(message.from_user.id, 'Выберете вид сортировки.', reply_markup=sort_keyboard())

        else:
            bot.send_message(message.from_user.id, 'Пожалуйста, нажмите на кнопку.', reply_markup=choice_params())


@bot.message_handler(state=CorrectRequestHighAndLowParams.terms, content_types=['text'])
def get_terms(message: Message) -> None:
    '''
    получает вид сортировки и запрашивает дату

    :param message: сообщение юзера
    :return:
    '''
    if back(message):
        if message.text == 'Сортировать по убыванию':
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data_user:
                data_user['condition'] = True
            bot.set_state(message.from_user.id, CorrectRequestHighAndLowParams.date, message.chat.id)
            bot.send_message(message.from_user.id, 'Выберете дату.', reply_markup=set_date())


        elif message.text == 'Сортировать по возрастанию':
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data_user:
                data_user['condition'] = False
            bot.set_state(message.from_user.id, CorrectRequestHighAndLowParams.date, message.chat.id)
            bot.send_message(message.from_user.id, 'Выберете дату.', reply_markup=set_date())

        else:
            bot.send_message(message.from_user.id, 'Пожалуйста, нажмите на кнопку.', reply_markup=sort_keyboard())


@bot.message_handler(state=CorrectRequestHighAndLowParams.date, content_types=['text'])
def get_date(message: Message):
    '''
    получает дату и запрашивает время

    :param message: сообщение юзера
    :return:
    '''
    if back(message):
        if message.text in full_date.keys():
            bot.set_state(message.from_user.id, CorrectRequestHighAndLowParams.time, message.chat.id)
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data_user:
                data_user['date'] = full_date[message.text]

            if message.text == 'Сегодня':
                bot.send_message(message.from_user.id, 'Теперь выберите интересующее время в часах', reply_markup=set_time_now())

            else:
                bot.send_message(message.from_user.id, 'Теперь выберите интересующее время в часах', reply_markup=set_time())

        else:
            bot.send_message(message.from_user.id, 'Пожалуйста, нажмите на кнопку.', reply_markup=set_date())


@bot.message_handler(state=CorrectRequestHighAndLowParams.time, content_types=['text'])
def get_time(message: Message) -> None:
    '''
    получает время и выводит ответ юзеру

    :param message: сообщение юзера
    :return:
    '''
    if back(message):
        user_time = message.text
        history = HistoryDB()
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data_user:
            date = data_user.get('date')
        today = tuple(full_date.values())[0]

        time_true = get_valid_time(True)
        if (user_time == 'Сейчас' and date == today) or (date != today and user_time in get_valid_time(False))\
                or ((date == today) and (time_true is not None) and (user_time in time_true)): # Проверка введенных данных

            if user_time == 'Сейчас':
                with bot.retrieve_data(message.from_user.id, message.chat.id) as data_user:
                    answer = select_top_towns_now(cities=data_user.get('cities'), params=data_user.get('params'),
                                                  condition=data_user.get('condition'))
                history.add_info(message.from_user.id, '/searchparams', answer)
                bot.delete_state(message.from_user.id, message.chat.id)
                bot.send_message(message.from_user.id, text=answer, reply_markup=buttons_for_help())

            else:
                with bot.retrieve_data(message.from_user.id, message.chat.id) as data_user:
                    answer = select_top_towns_predict(cities=data_user.get('cities'), period=f'{date} {user_time}',
                                                      params=data_user.get('params'), condition=data_user.get('condition'))

                history.add_info(message.from_user.id, '/searchparams', answer)
                bot.delete_state(message.from_user.id, message.chat.id)
                bot.send_message(message.from_user.id, text=answer, reply_markup=buttons_for_help())

        else:
            if date == today:
                bot.send_message(message.from_user.id, 'Пожалуйста, нажмите на кнопку.', reply_markup=set_time_now())

            else:
                bot.send_message(message.from_user.id, 'Пожалуйста, нажмите на кнопку.', reply_markup=set_time())








