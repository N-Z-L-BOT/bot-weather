from utills.set_bot_commands import setup_bot
from telebot.custom_filters import StateFilter
from loader import bot


if __name__ == '__main__':
    bot.add_custom_filter(StateFilter(bot))
    setup_bot()
    bot.polling()




