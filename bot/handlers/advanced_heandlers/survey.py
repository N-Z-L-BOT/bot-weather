from loader import bot
from states.user_state_survey import UserState
from telebot.types import Message
from keyboards.reply.advanced_keyboard import request_contact_user
from database.information_users_DB import DataUsers
from keyboards.reply.defoult_keboard import button_for_back, buttons_for_help, buttons_for_direction_survey, approved_for_survey, button_for_survey
from states.user_state_survey import back
from utills.beautiful_print import statistic


@bot.message_handler(commands=['survey'])
def start_survey(message: Message) -> None:
    '''
    требует выбрать действие

    :param message: сообщение юзера
    :return:
    '''
    bot.set_state(message.from_user.id, UserState.direction, message.chat.id)
    bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=buttons_for_direction_survey())


@bot.message_handler(state=UserState.direction, content_types=['text'])
def direction(message: Message) -> None:
    '''
    обрабатывает выбор или запрашивает подтверждение

    :param message: сообщение юзера
    :return:
    '''
    if back(message):
        if message.text == 'Просмотреть информацию о себе':
            USER = DataUsers()
            info = USER.get_data(message.from_user.id)
            if info:
                name, surname, age, country, town, phone, score = info[0][2], info[0][3], info[0][4], info[0][5],\
                    info[0][6], info[0][7], info[0][8]

                top = USER.get_score_players()
                ratio = statistic(top, score)

                answer = f'Информация о вас:\n' \
                         f'Имя: {name}\n' \
                         f'Фамилия: {surname}\n' \
                         f'Возраст: {age}\n' \
                         f'Страна: {country}\n' \
                         f'Город: {town}\n' \
                         f'Номер телефона: {phone}\n' \
                         f'Количество очков OpenWeather: {score} (результат лучше, чем у {ratio}% игроков!)'

                bot.delete_state(message.from_user.id, message.chat.id)
                bot.send_message(message.from_user.id, text=answer, reply_markup=buttons_for_help())

            else:
                bot.send_message(message.from_user.id, 'Информация не найдена, пожалуйста, пройдите опрос',
                                 reply_markup=buttons_for_direction_survey())

        elif message.text == 'Удалить информацию о себе':
            USER = DataUsers()
            if USER.exist_user(message.from_user.id):
                bot.set_state(message.from_user.id, UserState.approved, message.chat.id)
                bot.send_message(message.from_user.id, 'Вы уверены, что хотите удалить информацию о себе?'
                                                       ' Без нее многие команды будут недоступны.',
                                 reply_markup=approved_for_survey())

            else:
                bot.send_message(message.from_user.id, 'Информация не найдена, пожалуйста, пройдите опрос',
                                 reply_markup=buttons_for_direction_survey())

        elif message.text == 'Пройти опрос':
            bot.set_state(message.from_user.id, UserState.name, message.chat.id)
            bot.send_message(message.from_user.id, 'Пожалуйста, введите свое имя', reply_markup=button_for_back())

        else:
            bot.send_message(message.from_user.id, 'Пожалуйста, нажмите на кнопку', reply_markup=buttons_for_direction_survey())



@bot.message_handler(state=UserState.approved, content_types=['text'])
def approved(message: Message) -> None:
    '''
    удаляет информацию из базы данных

    :param message: сообщение юзера
    :return:
    '''
    if back(message):
        if message.text == 'Подтвердить':
            USER = DataUsers()
            USER.delete_data(message.from_user.id)
            bot.delete_state(message.from_user.id, message.chat.id)
            bot.send_message(message.from_user.id, 'Информация успешно удалена,'
                                                   ' чтобы вновь пользоваться ботом, пройдите опрос.',
                             reply_markup=button_for_survey())

        elif message.text == 'Отменить':
            bot.delete_state(message.from_user.id, message.chat.id)
            bot.send_message(message.from_user.id, 'Операция отменена.', reply_markup=buttons_for_help())

        else:
            bot.send_message(message.from_user.id, 'Пожалуйста, нажмите на кнопку', reply_markup=approved_for_survey())




@bot.message_handler(state=UserState.name)
def get_name_user(message: Message) -> None:
    '''
    записывает имя юзера

    :param message: сообщение юзера
    :return:
    '''
    if back(message):
        if message.text.isalpha():
            bot.send_message(message.from_user.id, f'Ответ записан. {message.text.title()},'
                                                   f' пожалуйста, введите свою фамилию', reply_markup=button_for_back())
            bot.set_state(message.from_user.id, UserState.surname, message.chat.id)

            with bot.retrieve_data(message.from_user.id, message.chat.id) as data_user:
                data_user['name'] = message.text.title()

        else:
            bot.send_message(message.from_user.id, f'Хм... Перепроверьте написание своего имени.'
                                                   f' Оно содержит нетривиальные символы.', reply_markup=button_for_back())


@bot.message_handler(state=UserState.surname)
def get_surname_user(message: Message) -> None:
    '''
    записывает фамилию юзера

    :param message: сообщение юзера
    :return:
    '''
    if back(message):
        if all((not(letter.isdigit())) for letter in message.text):
            bot.send_message(message.from_user.id, 'Принято. Теперь введите свой возраст', reply_markup=button_for_back())
            bot.set_state(message.from_user.id, UserState.age, message.chat.id)

            with bot.retrieve_data(message.from_user.id, message.chat.id) as data_user:
                data_user['surname'] = message.text.title()

        else:
            bot.send_message(message.from_user.id, f'Фамилия не должна содержать цифры.', reply_markup=button_for_back())


@bot.message_handler(state=UserState.age)
def get_age_user(message: Message) -> None:
    '''
    записывает возраст юзера

    :param message: сообщение юзера
    :return:
    '''
    if back(message):
        if message.text.isdigit():
            age = int(message.text)
            if age in range(3, 130):
                bot.send_message(message.from_user.id, f'Записал. Введите страну проживания.', reply_markup=button_for_back())
                bot.set_state(message.from_user.id, UserState.country, message.chat.id)

                with bot.retrieve_data(message.from_user.id, message.chat.id) as data_user:
                    data_user['age'] = age

            else:
                bot.send_message(message.from_user.id, f'Какой - то неправдоподобный возраст. Попробуйте снова.',
                                 reply_markup=button_for_back())

        else:
            bot.send_message(message.from_user.id, f'Удивительный возраст! Обычно он содержит только цифры.'
                                                   f' Попробуйте еще раз.', reply_markup=button_for_back())


@bot.message_handler(state=UserState.country)
def get_country_user(message: Message) -> None:
    '''
    записывает страну юзера

    :param message: сообщение юзера
    :return:
    '''
    if back(message):
        if all((not(letter.isdigit())) for letter in message.text):
            bot.send_message(message.from_user.id, f'Понял. Введите свой город.', reply_markup=button_for_back())
            bot.set_state(message.from_user.id, UserState.town, message.chat.id)

            with bot.retrieve_data(message.from_user.id, message.chat.id) as data_user:
                data_user['country'] = message.text.title()

        else:
            bot.send_message(message.from_user.id, f'Страна не содержит цифр', reply_markup=button_for_back())


@bot.message_handler(state=UserState.town)
def get_town_user(message: Message) -> None:
    '''
    записывает город юзера

    :param message: сообщение юзера
    :return:
    '''
    if back(message):
        if all((not(letter.isdigit())) for letter in message.text):
            bot.send_message(message.from_user.id,
                             f'Хорошо. Крайний шаг. Отправьте свой номер телефона, нажав на появившуюся кнопку.',
                             reply_markup=request_contact_user())


            bot.set_state(message.from_user.id, UserState.phone_number, message.chat.id)
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data_user:
                data_user['town'] = message.text.title()

        else:
            bot.send_message(message.from_user.id, f'Город не должен содержать цифры', reply_markup=button_for_back())


@bot.message_handler(content_types=['text', 'contact'], state=UserState.phone_number)
def get_phone_number_user(message: Message) -> None:
    '''
    записывает номер юзера

    :param message: сообщение юзера
    :return:
    '''
    if back(message):
        if message.content_type == 'contact':
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data_user:
                data_user['phone'] = str(message.contact.phone_number)
                answer = f'Спасибо за информацию. Ваши данные:\n' \
                         f'Имя: {data_user["name"]}\n' \
                         f'Фамилия: {data_user["surname"]}\n' \
                         f'Возраст: {data_user["age"]}\n' \
                         f'Страна: {data_user["country"]}\n' \
                         f'Город: {data_user["town"]}\n' \
                         f'Номер телефона: {data_user["phone"]}\n' \
                         f'Количество очков OpenWeather: 0 (результат лучше, чем у 0% игроков!)'
                bot.send_message(message.from_user.id, answer, reply_markup=buttons_for_help())
                USER = DataUsers()
                if USER.exist_user(message.from_user.id):
                    USER.update_data(message.from_user.id, data_user=data_user)

                else:
                    USER.add_info(message.from_user.id, data_user=data_user)

            bot.delete_state(message.from_user.id, message.chat.id)

        else:
            bot.send_message(message.from_user.id, 'Пожалуйста, нажмите на кнопку', reply_markup=request_contact_user())















