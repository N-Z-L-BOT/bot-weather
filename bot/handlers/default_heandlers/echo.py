from loader import bot
from telebot.types import Message
from keyboards.reply.defoult_keboard import button_for_echo, buttons_for_help


@bot.message_handler()
def echo(message: Message) -> None:
    '''
    Сообщает об ошибке и перенаправлет на другую команду

    :param message: Сообщение юзера
    :return:
    '''
    if message.text == 'Вернуться в меню':
        bot.send_message(message.from_user.id, 'Выберете действие.', reply_markup=buttons_for_help())

    else:
        bot.reply_to(message, 'Я вас не понял😢, пожалуйста, введите команду /help😃', reply_markup=button_for_echo())
