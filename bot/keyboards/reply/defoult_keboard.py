from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def buttons_for_start() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(True, True)
    button1 = KeyboardButton(text='/survey')
    button2 = KeyboardButton(text='/help')
    keyboard.add(button1, button2)
    return keyboard


def buttons_for_help() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(True, True)
    buttons = (KeyboardButton('/survey'),
               KeyboardButton('/infocity'),
               KeyboardButton('/searchparams'),
               KeyboardButton('/event'),
               KeyboardButton('/history'))
    keyboard.add(*buttons)
    return keyboard


def button_for_echo() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(True, True)
    button = KeyboardButton(text='/help')
    keyboard.add(button)
    return keyboard


def button_for_back() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(True, True)
    button = KeyboardButton('Вернуться в меню')
    keyboard.add(button)
    return keyboard


def button_for_survey() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(True, True)
    button = KeyboardButton('/survey')
    keyboard.add(button, KeyboardButton(text='Вернуться в меню'))
    return keyboard


def buttons_for_history() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    browse = KeyboardButton('Просмотреть историю')
    delete = KeyboardButton('Удалить историю')
    keyboard.add(browse, delete, KeyboardButton('Вернуться в меню'))
    return keyboard


def buttons_for_direction_survey() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    survey = KeyboardButton(text='Пройти опрос')
    browse = KeyboardButton(text='Просмотреть информацию о себе')
    delete = KeyboardButton(text='Удалить информацию о себе')
    keyboard.add(survey, browse, delete, KeyboardButton(text='Вернуться в меню'))
    return keyboard


def approved_for_survey() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    proved = KeyboardButton(text='Подтвердить')
    cancel = KeyboardButton(text='Отменить')
    keyboard.add(proved, cancel, KeyboardButton(text='Вернуться в меню'))
    return keyboard
