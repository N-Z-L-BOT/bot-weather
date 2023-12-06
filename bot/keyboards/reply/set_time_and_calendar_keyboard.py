from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from utills.date_and_time import get_valid_time
from utills.date_and_time import full_date


def generate_button(now: bool = True) -> tuple[KeyboardButton] | None:
    '''

    :param now: принимает булево значение (в зависимости от того, какую дату выбрал пользователь)
    :return: возваращет кнопки или None
    '''
    all_button = get_valid_time(now)
    if all_button is not None:
        return tuple(KeyboardButton(text=n) for n in all_button)
    return None


def set_time_now() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(True, True)
    all_button = generate_button()
    if all_button is None:
        keyboard.add('Сейчас', KeyboardButton(text='Вернуться в меню'))
    else:
        keyboard.add('Сейчас', *all_button, KeyboardButton(text='Вернуться в меню'))
    return keyboard


def set_time() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(True, True)
    keyboard.add(*generate_button(False), KeyboardButton(text='Вернуться в меню'))
    return keyboard


def set_date() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(True, True)
    buttons = (KeyboardButton(text=key) for key in full_date.keys())
    keyboard.add(*buttons, KeyboardButton(text='Вернуться в меню'))
    return keyboard



