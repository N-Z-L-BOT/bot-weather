from telebot.handler_backends import State, StatesGroup

class CheckHistory(StatesGroup):
    choice_parted = State()
    constraint = State()
