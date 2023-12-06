from loader import bot
from telebot.types import Message
from states.history_state import CheckHistory
from database.data_on_requests_and_responses_DB import HistoryDB
from database.information_users_DB import DataUsers
from states.user_state_survey import back
from keyboards.reply.defoult_keboard import button_for_survey, buttons_for_help, button_for_back, buttons_for_history


@bot.message_handler(commands=['history'])
def history(message: Message) -> None:
    '''
    проверяет юзера по БД и предоставляет выбор для дальнейших действий

    :param message: сообщение юзера
    :return:
    '''
    USER = DataUsers()
    if USER.exist_user(message.from_user.id):
        bot.set_state(message.from_user.id, CheckHistory.choice_parted, message.chat.id)
        bot.send_message(message.from_user.id, 'Хотите просмотреть историю или удалить ее?', reply_markup=buttons_for_history())

    else:
        bot.send_message(message.from_user.id, 'Чтобы использовать бота, пожалуйста, пройдите опрос /survey', reply_markup=button_for_survey())


@bot.message_handler(content_types=['text'], state=CheckHistory.choice_parted)
def get_limit(message: Message) -> None:
    '''
    обрабатывает запрос и спрашивает о дальнейших шагах

    :param message: сообщение юзера
    :return:
    '''
    if back(message):
        if message.text == 'Удалить историю':
            history = HistoryDB()
            history.delete_history(message.from_user.id)
            bot.send_message(message.from_user.id, 'История успешно удалена.', reply_markup=buttons_for_help())
            bot.delete_state(message.from_user.id, message.chat.id)

        elif message.text == 'Просмотреть историю':

            bot.send_message(message.from_user.id, 'Напишите количество последних запросов, которых нужно вывести',
                             reply_markup=button_for_back())
            bot.set_state(message.from_user.id, CheckHistory.constraint, message.chat.id)

        else:
            bot.send_message(message.from_user.id, 'Пожалуйста, нажмите на кнопку', reply_markup=buttons_for_history())


@bot.message_handler(state=CheckHistory.constraint)
def get_constraint(message: Message) -> None:
    '''
    выводит историю

    :param message: сообщение юзера
    :return:
    '''
    if back(message):
        if message.text.isdigit():
            history = HistoryDB()
            full_history = history.get_data(message.from_user.id)
            if full_history:

                for total, info in enumerate(full_history[::-1]):
                    if total == int(message.text):
                        break

                    else:
                        command, answer = info[1], info[2]
                        bot.delete_state(message.from_user.id, message.chat.id)
                        bot.send_message(message.from_user.id, f'Команда: {command}\n\n'
                                                               f'Ответ бота: {answer}', reply_markup=buttons_for_help())
            else:
                bot.send_message(message.from_user.id, 'История пуста', reply_markup=buttons_for_help())


        else:
            bot.send_message(message.from_user.id, 'Количество - это число. Попробуйте снова', reply_markup=button_for_back())

