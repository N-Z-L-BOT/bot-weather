from telebot.handler_backends import State, StatesGroup


class CorrectRequestInfoCity(StatesGroup):
    city = State()
    date = State()
    time = State()


class CorrectRequestHighAndLowParams(StatesGroup):
    cities = State()
    params = State()
    terms = State()
    date = State()
    time = State()





