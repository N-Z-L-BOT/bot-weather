import sqlite3
import datetime

class DataUsers:
    def __init__(self, file_db='USERS.db'):
        self.__connect = sqlite3.connect(file_db)
        self.__cursor = self.__connect.cursor()
        self.__setup_database()

    def __setup_database(self):
        '''

        :return: Создает базу данных, содержащую информацию о юзере
        '''
        with self.__connect:
            return self.__cursor.execute(f'''CREATE TABLE IF NOT EXISTS users_data (
            user_ID INT, 
            date_registration datetime,
            name TEXT,
            surname TEXT,
            age INT,
            country TEXT,
            town TEXT,
            phone_number TEXT,
            score INT)
            ''')

    def add_info(self, id: int, data_user: dict):
        '''

        :param id: ид юзера
        :param data_user: словарь, содержащий данные о юзере
        :return: добавляет данные в базу
        '''
        with self.__connect:
            return self.__cursor.execute('''INSERT INTO users_data(
            `user_ID`, 
            `date_registration`,
            `name`,
            `surname`,
            `age`,
            `country`,
            `town`,
            `phone_number`,
            `score`)
            VALUES (?,?,?,?,?,?,?,?,?)''', (id, datetime.datetime.now(), data_user.get('name'), data_user.get('surname'),
                                     data_user.get('age'), data_user.get('country'), data_user.get('town'),
                                            data_user.get('phone'), 0))

    def update_data(self, id: int, data_user: dict):
        '''

        :param id: изер ид
        :param data_user: словарь, содержащий данные о юзере
        :return: обнавляет данные о юзере
        '''
        with self.__connect:
            return self.__cursor.execute('''UPDATE users_data SET
            `name` = ?,
            `surname` = ?,
            `age` = ?,
            `country` = ?,
            `town` = ?,
            `phone_number` = ?
            WHERE user_ID = ?''', (data_user['name'], data_user['surname'],
                                     data_user['age'], data_user['country'], data_user['town'], data_user['phone'], id))

    def exist_user(self, id: int) -> bool:
        '''

        :param id: изер ид
        :return: возвращает True или False в зависимости от наличия юзера в бд
        '''
        with self.__connect:
            values = self.__cursor.execute('''SELECT 
            `user_ID` FROM users_data WHERE `user_ID` = ?''', (id,))
            return bool(len(values.fetchall()))

    def delete_data(self, id: int):
        '''

        :param id: ид юзера
        :return: удаляет данные о юзере
        '''
        with self.__connect:
            return self.__cursor.execute('''DELETE FROM users_data WHERE `user_ID` = ?''', (id,))

    def get_data(self, id: int) -> list:
        '''

        :param id: ид юзера
        :return: возвращает данные о юзере
        '''
        with self.__connect:
            data = self.__cursor.execute('''SELECT * FROM users_data
            WHERE `user_ID` == ?''', (id,))
            return data.fetchall()

    def update_score(self, id: int, score: int):
        '''

        :param id: ид юзера
        :param score: очки юзера
        :return: обновляет очки OpenWeather юзера
        '''
        with self.__connect:
            score_old = self.get_data(id)[0][8]
            new_score = score_old + score
            return self.__cursor.execute('''UPDATE users_data SET
            `score` = ?
            WHERE user_ID = ?''', (new_score, id))

    def get_score_players(self) -> list:
        '''

        :return: возвращает все очки OpenWeather всех юзеров
        '''
        with self.__connect:
            scores = self.__cursor.execute('''SELECT `score` FROM users_data''')
            return scores.fetchall()











