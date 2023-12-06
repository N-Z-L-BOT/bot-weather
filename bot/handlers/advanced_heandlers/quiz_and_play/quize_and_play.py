from loader import bot
from keyboards.reply.advanced_keyboard import quiz_or_play_keyboard, lucky_keyboard, distributed_answer
from keyboards.reply.defoult_keboard import button_for_back, buttons_for_help
from states.user_state_survey import EventState
from telebot.types import Message
from database.information_users_DB import DataUsers
from handlers.advanced_heandlers.quiz_and_play.generator_issues import get_question_and_responses_and_right,\
    count_right_response
from states.user_state_survey import back
import random


@bot.message_handler(commands=['event'])
def event(message: Message) -> None:
    '''
    требует выбор действия
    :param message: сообщение юзера
    :return:
    '''

    bot.set_state(message.from_user.id, EventState.path, message.chat.id)
    bot.send_message(message.from_user.id, 'Выберете действие.', reply_markup=quiz_or_play_keyboard(message.from_user.id))


@bot.message_handler(state=EventState.path, content_types=['text'])
def path(message: Message) -> None:
    '''
    Обрабатывает ответ и создает состояния для дальнейших команд

    :param message: сообщение юзера
    :return:
    '''
    if back(message):
        if message.text == 'Получить доступ к боту и очки OpenWeather😀':
            bot.set_state(message.from_user.id, EventState.digit_bot_medium, message.chat.id)
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data_user:
                data_user['digit'] = random.randint(1, 10)

            bot.send_message(message.from_user.id, 'Чтобы получить доступ к продвинутым командам, отгадайте мое число.'
                                                   ' Оно в пределах от 1 до 10 включительно.', reply_markup=button_for_back())

        elif message.text == 'Ответить на вопросы веселой викторины!':
            USER = DataUsers()
            if USER.exist_user(message.from_user.id):
                text, variants, answer = get_question_and_responses_and_right(0)
                bot.set_state(message.from_user.id, EventState.issue1, message.chat.id)
                with bot.retrieve_data(message.from_user.id, message.chat.id) as data_user:
                    data_user['right1'] = answer
                bot.send_message(message.from_user.id, f'Первый вопрос:\n\n{text}\nВарианты ответов:\n\n{variants}',
                                 reply_markup=distributed_answer())
            else:
                bot.send_message(message.from_user.id, 'Пожалуйста, пройдите опрос или выиграйте доступ к этой функции!',
                                 reply_markup=quiz_or_play_keyboard(message.from_user.id))


        elif message.text == 'Испытать удачу и выиграть гору очков OpenWeather!':
            USER = DataUsers()
            if USER.exist_user(message.from_user.id):
                bot.set_state(message.from_user.id, EventState.choice_complexity, message.chat.id)
                bot.send_message(message.from_user.id, 'Выберите сложность игры.', reply_markup=lucky_keyboard())
            else:
                bot.send_message(message.from_user.id, 'Пожалуйста, пройдите опрос или выиграйте доступ к этой функции!',
                                 reply_markup=quiz_or_play_keyboard(message.from_user.id))


        else:
            bot.send_message(message.from_user.id, 'Пожалуйста, нажмите на кнопку',
                             reply_markup=quiz_or_play_keyboard(message.from_user.id))


@bot.message_handler(state=EventState.choice_complexity, content_types=['text'])
def get_complexity(message: Message) -> None:
    '''
    обрабатывает сложность

    :param message: сообщение юзера
    :return:
    '''
    if back(message):
        if message.text == 'Нормально (100 очков)😄':
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data_user:
                data_user['digit'] = random.randint(1, 10)

            bot.set_state(message.from_user.id, EventState.digit_bot_medium, message.chat.id)
            bot.send_message(message.from_user.id, 'Я загадал число от 1 до 10. Попробуй его отгадать!',
                             reply_markup=button_for_back())

        elif message.text == 'Сложно (10 000 очков)😮':
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data_user:
                data_user['digit'] = random.randint(1, 100)

            bot.set_state(message.from_user.id, EventState.digit_bot_hard, message.chat.id)
            bot.send_message(message.from_user.id, 'Я загадал число от 1 до 100. Попробуй его отгадать!',
                             reply_markup=button_for_back())

        elif message.text == 'Невозможно (1 000 000 очков)😢':
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data_user:
                data_user['digit'] = random.randint(1, 1000)

            bot.set_state(message.from_user.id, EventState.digit_bot_impossible, message.chat.id)
            bot.send_message(message.from_user.id, 'Я загадал число от 1 до 1000. Попробуй его отгадать!',
                             reply_markup=button_for_back())

        else:
            bot.send_message(message.from_user.id, 'Пожалуйста, нажмите на кнопку.', reply_markup=lucky_keyboard())


@bot.message_handler(state=EventState.digit_bot_hard)
def get_score_hard(message: Message) -> None:
    '''
    анализирует число пользователя и добавляет очки юзеру

    :param message: сообщение юзера
    :return:
    '''
    if back(message):
        if message.text.isdigit():
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data_user:
                great_result = data_user.get('digit')
            if great_result == int(message.text):
                USER = DataUsers()
                USER.update_score(message.from_user.id, 10_000)
                bot.delete_state(message.from_user.id, message.chat.id)
                bot.send_message(message.from_user.id, 'Поздравляю! Вы выиграли 10 000 очков OpenWeather! Буду ждать вас снова!',
                                 reply_markup=buttons_for_help())

            else:
                bot.delete_state(message.from_user.id, message.chat.id)
                bot.send_message(message.from_user.id, f'НЕУДАЧА! Загаданное число - {great_result}. Попробуйте снова!', reply_markup=buttons_for_help())
        else:
            bot.send_message(message.from_user.id, 'Введите число.', reply_markup=button_for_back())


@bot.message_handler(state=EventState.digit_bot_medium, content_types=['text'])
def get_score_and_access_medium(message: Message) -> None:
    '''
    записывает пользователя в БД и добавляет ему очки

    :param message: сообщение юзера
    :return:
    '''
    if back(message):
        if message.text.isdigit():
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data_user:
                great_result = data_user.get('digit')
            if great_result == int(message.text):
                USER = DataUsers()
                if not USER.exist_user(message.from_user.id):
                    data = {'name': 'WINNER!', 'surname': 'WINNER!', 'age': 0, 'country': 'WINNER!',
                            'town': 'WINNER', 'phone': 'WINNER!'}
                    USER.add_info(message.from_user.id, data_user=data)
                    bot.send_message(message.from_user.id,
                                     'Поздравляю! Вы получили полный доступ ко всем функциям бота!',)
                USER.update_score(message.from_user.id, 100)
                bot.delete_state(message.from_user.id, message.chat.id)
                bot.send_message(message.from_user.id, 'Поздравляю! Вы выиграли 100 очков OpenWeather! Буду ждать вас снова!',
                                 reply_markup=buttons_for_help())

            else:
                bot.delete_state(message.from_user.id, message.chat.id)
                bot.send_message(message.from_user.id, f'НЕУДАЧА! Загаданное число - {great_result}. Попробуйте снова!',
                                 reply_markup=buttons_for_help())
        else:
            bot.send_message(message.from_user.id, 'Введите число.', reply_markup=button_for_back())


@bot.message_handler(state=EventState.digit_bot_impossible, content_types=['text'])
def get_score_impossible(message: Message) -> None:
    '''
    анализирует число пользователя и добавляет очки юзеру

    :param message: сообщение юзера
    :return:
    '''
    if back(message):
        if message.text.isdigit():
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data_user:
                great_result = data_user.get('digit')

            if great_result == int(message.text):
                USER = DataUsers()
                USER.update_score(message.from_user.id, 1_000_000)
                bot.delete_state(message.from_user.id, message.chat.id)
                bot.send_message(message.from_user.id, 'Поздравляю! Вы сделали практически невозможное!'
                                                       '\nДобавлено очков OpenWeather: 1 000 000!\nБуду ждать вас снова!',
                                 reply_markup=buttons_for_help())
            else:
                bot.delete_state(message.from_user.id, message.chat.id)
                bot.send_message(message.from_user.id, f'НЕУДАЧА! Загаданное число - {great_result}. Попробуйте снова!',
                                 reply_markup=buttons_for_help())
        else:
            bot.send_message(message.from_user.id, 'Введите число.', reply_markup=button_for_back())


@bot.message_handler(state=EventState.issue1, content_types=['text'])
def get_answer_1(message: Message) -> None:
    '''
    анализирует ответ юзера и задает второй вопрос

    :param message: сообщение пользователя
    :return:
    '''
    if back(message):
        if message.text in ("А", "Б", "В"):
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data_user:
                data_user['response1'] = message.text == data_user.get('right1')


            text, variants, answer = get_question_and_responses_and_right(1)
            bot.set_state(message.from_user.id, EventState.issue2, message.chat.id)
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data_user:
                data_user['right2'] = answer
            bot.send_message(message.from_user.id, f'Второй вопрос:\n\n{text}\nВарианты ответов:\n\n{variants}',
                             reply_markup=distributed_answer())
        else:
            bot.send_message(message.from_user.id, 'Пожалуйста, нажмите на кнопку', reply_markup=distributed_answer())


@bot.message_handler(state=EventState.issue2, content_types=['text'])
def get_answer_2(message: Message) -> None:
    '''
    анализирует ответ юзера и задает третий вопрос

    :param message: сообщение юзера
    :return:
    '''
    if back(message):
        if message.text in ("А", "Б", "В"):
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data_user:
                data_user['response2'] = message.text == data_user.get('right2')


            text, variants, answer = get_question_and_responses_and_right(2)
            bot.set_state(message.from_user.id, EventState.issue3, message.chat.id)
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data_user:
                data_user['right3'] = answer
            bot.send_message(message.from_user.id, f'Третий вопрос:\n\n{text}\nВарианты ответов:\n\n{variants}',
                             reply_markup=distributed_answer())
        else:
            bot.send_message(message.from_user.id, 'Пожалуйста, нажмите на кнопку', reply_markup=distributed_answer())


@bot.message_handler(state=EventState.issue3, content_types=['text'])
def get_answer_3_and_count_answer(message: Message) -> None:
    '''
    анализирует ответ юзера, предоставляет информацию об ответах и добавляет очки юзеру

    :param message: сообщение юзера
    :return:
    '''
    if back(message):
        if message.text in ("А", "Б", "В"):
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data_user:
                data_user['response3'] = message.text == data_user.get('right3')
                answer, count = count_right_response(data=data_user)

            USER = DataUsers()
            USER.update_score(message.from_user.id, count)
            bot.send_message(message.from_user.id, answer, reply_markup=buttons_for_help())

        else:
            bot.send_message(message.from_user.id, 'Пожалуйста, нажмите на кнопку', reply_markup=distributed_answer())





























