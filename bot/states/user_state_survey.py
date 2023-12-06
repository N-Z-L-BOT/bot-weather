from telebot.handler_backends import State, StatesGroup
from telebot.types import Message, CallbackQuery
from loader import bot
from keyboards.reply.defoult_keboard import buttons_for_help



class UserState(StatesGroup):
    direction = State()
    approved = State()
    name = State()
    surname = State()
    age = State()
    country = State()
    town = State()
    phone_number = State()


def back(message: Message | CallbackQuery) -> bool:
    '''

    :param message: принимает либо сообщение юзера либо кэлбэк от нажатия на кнопку
    :return: сбрасывает все состояния
    '''
    if type(message) is CallbackQuery:
        if message.data == 'Вернуться в меню':
            bot.delete_state(message.message.chat.id, message.message.from_user.id)
            bot.send_message(message.message.chat.id, 'Состояние успешно сброшено', reply_markup=buttons_for_help())
            return False

    elif message.text == 'Вернуться в меню':
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.send_message(message.from_user.id, 'Состояние успешно сброшено.', reply_markup=buttons_for_help())
        return False

    return True


class EventState(StatesGroup):
    path = State()
    choice_complexity = State()
    digit_bot_medium = State()
    digit_bot_hard = State()
    digit_bot_impossible = State()
    issue1 = State()
    issue2 = State()
    issue3 = State()






