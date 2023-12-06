from dotenv import find_dotenv, load_dotenv
import os

if not find_dotenv():
    exit('Пожалуйста, создайте файл ".env" с переменными окружения для работы бота.')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')


