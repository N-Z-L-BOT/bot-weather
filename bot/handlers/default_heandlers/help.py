from loader import bot
from keyboards.reply.defoult_keboard import buttons_for_help
from telebot.types import Message


@bot.message_handler(commands=['help'])
def help_user(message: Message) -> None:
    '''
    рассказывает о всех командах

    :param message: принимает сообщение юзера
    :return:
    '''
    bot.send_message(message.chat.id, f'Чтобы пройти опрос и пользоваться командами бота, введите /survey😀\n\n'
                                      f'Команда /infocity поможет вам узнать подробную информацию о погоде в конкретном месте\n'
                                      f'Команда /searchparams отсортирует города по нужным параматерам\n'
                                      f'Команда /event отвечат за викторину и другие бонусы!\n'
                                      f'Команда /history покажет историю запросов и ответов',

                     reply_markup=buttons_for_help())
