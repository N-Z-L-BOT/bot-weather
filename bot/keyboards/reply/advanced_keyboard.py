from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from database.information_users_DB import DataUsers


def generate_buttons_for_event(id: int) -> KeyboardButton:
    USER = DataUsers()
    if USER.exist_user(id):
        return KeyboardButton(text='Испытать удачу и выиграть гору очков OpenWeather!')
    return KeyboardButton(text='Получить доступ к боту и очки OpenWeather😀')


def request_contact_user() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(True, True)
    keyboard.add(KeyboardButton(text='Отправить номер телефона', request_contact=True), KeyboardButton(text='Вернуться в меню'))
    return keyboard


def choice_params() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    temperature = KeyboardButton(text='Температура')
    duration_day = KeyboardButton(text='Продолжительность дня')
    keyboard.add(temperature, duration_day, KeyboardButton(text='Вернуться в меню'))
    return keyboard


def sort_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    descend = KeyboardButton(text='Сортировать по убыванию')
    ascend = KeyboardButton(text='Сортировать по возрастанию')
    keyboard.add(descend, ascend, KeyboardButton(text='Вернуться в меню'))
    return keyboard


def quiz_or_play_keyboard(id: int) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    lucky = generate_buttons_for_event(id)
    quiz = KeyboardButton('Ответить на вопросы веселой викторины!')
    keyboard.add(lucky, quiz, KeyboardButton(text='Вернуться в меню'))
    return keyboard


def lucky_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    medium = KeyboardButton(text='Нормально (100 очков)😄')
    hard = KeyboardButton(text='Сложно (10 000 очков)😮')
    impossible = KeyboardButton(text='Невозможно (1 000 000 очков)😢')
    keyboard.add(medium, hard, impossible, KeyboardButton(text='Вернуться в меню'))
    return keyboard


def distributed_answer() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(True, True)
    keyboard.add(KeyboardButton("А"), KeyboardButton("Б"), KeyboardButton("В"), KeyboardButton("Вернуться в меню"))
    return keyboard




