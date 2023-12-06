from loader import bot
from telebot.types import Message
from states.information_city_state import CorrectRequestInfoCity
from utills.API_request.info_weather_now import analytics_weather
from database.information_users_DB import DataUsers
from database.data_on_requests_and_responses_DB import HistoryDB
from keyboards.reply.set_time_and_calendar_keyboard import set_time_now, set_time, set_date
from utills.date_and_time import full_date, get_valid_time
from utills.API_request.predict_weather import predict_analytics_weather
from keyboards.reply.defoult_keboard import buttons_for_help, button_for_back, button_for_survey
from states.user_state_survey import back



@bot.message_handler(commands=['infocity'])
def infocity(message: Message) -> None:
    '''
    проеверяет юзера по БД и запрашивает город

    :param message: сообщение юзера
    :return:
    '''
    USER = DataUsers()
    if USER.exist_user(message.from_user.id):
        bot.set_state(message.from_user.id, CorrectRequestInfoCity.city, message.chat.id)
        bot.send_message(message.from_user.id, 'Напишите город.', reply_markup=button_for_back())
    else:
        bot.send_message(message.from_user.id, 'Чтобы использовать бота, пожалуйста, пройдите опрос /survey', reply_markup=button_for_survey())


@bot.message_handler(state=CorrectRequestInfoCity.city)
def get_town(message: Message) -> None:
    '''
    запрашивает дату для поиска

    :param message: сообщение юзера
    :return:
    '''
    if back(message):
        if all((not(letter.isdigit())) for letter in message.text):
            bot.set_state(message.from_user.id, CorrectRequestInfoCity.date, message.chat.id)
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data_user:
                data_user['city'] = message.text.capitalize()

            bot.send_message(message.from_user.id, 'Пожалуйста, выберите дату.', reply_markup=set_date())

        else:
            bot.send_message(message.from_user.id, 'Город не должен содержать цифры.', reply_markup=button_for_back())


@bot.message_handler(state=CorrectRequestInfoCity.date, content_types=['text'])
def get_date(message: Message) -> None:
    '''
    запрашивает время для поиска

    :param message: сообщение юзера
    :return:
    '''
    if back(message):
        if message.text in full_date.keys():
            bot.set_state(message.from_user.id, CorrectRequestInfoCity.time, message.chat.id)
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data_user:
                data_user['date'] = full_date[message.text]

            if message.text == 'Сегодня':
                bot.send_message(message.from_user.id, 'Теперь выберите интересующее время в часах.', reply_markup=set_time_now())
            else:
                bot.send_message(message.from_user.id, 'Теперь выберите интересующее время в часах.', reply_markup=set_time())

        else:
            bot.send_message(message.from_user.id, 'Пожалуйста, нажмите на кнопку.', reply_markup=set_date())




@bot.message_handler(state=CorrectRequestInfoCity.time, content_types=['text'])
def get_time(message: Message) -> None:
    '''
    возвращает обработанную информацию

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
                    answer = analytics_weather(city=data_user.get('city'), method='weather')
                history.add_info(message.from_user.id, '/infocity', answer)
                bot.send_message(message.from_user.id, answer, reply_markup=buttons_for_help())
                bot.delete_state(message.from_user.id, message.chat.id)

            else:
                with bot.retrieve_data(message.from_user.id, message.chat.id) as data_user:
                    answer = predict_analytics_weather(city=data_user.get('city'), method='forecast', period=f'{data_user.get("date")} {user_time}')

                history.add_info(message.from_user.id, '/infocity', answer)
                bot.send_message(message.from_user.id, answer, reply_markup=buttons_for_help())
                bot.delete_state(message.from_user.id, message.chat.id)

        else:

            if date == today:
                bot.send_message(message.from_user.id, 'Пожалуйста, нажмите на кнопку.', reply_markup=set_time_now())

            else:
                bot.send_message(message.from_user.id, 'Пожалуйста, нажмите на кнопку.', reply_markup=set_time())
