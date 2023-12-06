from loader import bot
from telebot.types import Message
from keyboards.reply.defoult_keboard import buttons_for_start


@bot.message_handler(commands=['start'])
def start(message: Message) -> None:
    '''
    встречает юзера и дает дальнейшие инструкции для использования

    :param message: сообщение юзера
    :return:
    '''
    bot.send_message(message.chat.id, f'Приветствую, {message.from_user.first_name}!\n'
                                      f'Я - один из лучший ботов современности, который поможет вам спрогнозировать'
                                      f' погоду в нужном городе или даже в нескольких городах сразу на 1/10 000 века вперед,'
                                      f' ведь использую для поиска API сайта OpenWeather!\n'
                                      f'Пожалуйста, введите команду /survey и пройдите маленький опрос,'
                                      f' а затем /help, чтобы узнать подробности обо мне!☺',
                     reply_markup=buttons_for_start())

