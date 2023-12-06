import sqlite3


class HistoryDB:
    def __init__(self, file_db='USERS.db'):
        self.__connect = sqlite3.connect(file_db)
        self.__cursor = self.__connect.cursor()
        self.__setup_database()

    def __setup_database(self):
        '''

        :return: Создание базы данных, содержащей историю поиска
        '''
        with self.__connect:
            return self.__cursor.execute(f'''CREATE TABLE IF NOT EXISTS users_history (
            user_ID INT,
            commands TEXT,
            answers_bot TEXT)
            ''')

    def add_info(self, id: int, actions: str, response_bot: str):
        '''

        :param id: ид юзера
        :param actions: команда бота
        :param response_bot: ответ бота
        :return: добавляет данные в базу
        '''
        with self.__connect:
            return self.__cursor.execute('''INSERT INTO users_history(
             `user_ID`,
             `commands`,
             `answers_bot`)
             VALUES (?,?,?)''', (id, actions, response_bot))

    def get_data(self, id: int) -> list:
        '''

        :param id: изер ид
        :return: возвращает данные юзере
        '''
        with self.__connect:
            data = self.__cursor.execute('''SELECT * FROM users_history
            WHERE `user_ID` == ?''', (id,))
            return data.fetchall()

    def delete_history(self, id: int):
        '''

        :param id: ид юзера
        :return: удаляет всю историю
        '''
        with self.__connect:
            return self.__cursor.execute('''DELETE FROM users_history WHERE `user_ID` = ?''', (id,))





